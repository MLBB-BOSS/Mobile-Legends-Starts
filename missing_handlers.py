from texts import TextTemplates  # Імпортуємо клас
from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from aiogram.fsm.context import FSMContext
import logging
from states import MenuStates

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class TransitionType(Enum):
    """Типи переходів між станами"""
    NORMAL = "normal"      # Звичайний перехід
    FORCED = "forced"      # Примусовий перехід
    ROLLBACK = "rollback"  # Повернення до попереднього стану
    RESET = "reset"        # Повне скидання стану

@dataclass
class StateTransitionResult:
    """Результат переходу між станами"""
    success: bool
    previous_state: Optional[str]
    new_state: str
    timestamp: datetime
    transition_type: TransitionType
    preserved_data: Dict[str, Any]
    error: Optional[str] = None

class StateManager:
    """Менеджер управління станами"""
    
    def __init__(self):
        self.state_history: List[Dict[str, Any]] = []
        self.max_history_size: int = 10
    
    async def _save_to_history(self, 
                             previous_state: str, 
                             new_state: str, 
                             data: Dict[str, Any]) -> None:
        """Зберігає історію переходів"""
        history_entry = {
            "from_state": previous_state,
            "to_state": new_state,
            "timestamp": datetime.utcnow(),
            "data": data
        }
        self.state_history.append(history_entry)
        
        # Обмеження розміру історії
        if len(self.state_history) > self.max_history_size:
            self.state_history.pop(0)

    async def transition_state(
        self,
        state: FSMContext,
        new_state: MenuStates,
        transition_type: TransitionType = TransitionType.NORMAL,
        preserve_data: bool = False,
        additional_data: Optional[Dict[str, Any]] = None,
        clear_specific: Optional[List[str]] = None
    ) -> StateTransitionResult:
        """
        Основна функція переходу між станами
        
        Args:
            state: FSMContext - контекст стану
            new_state: MenuStates - новий стан
            transition_type: TransitionType - тип переходу
            preserve_data: bool - зберегти поточні дані
            additional_data: Dict - додаткові дані
            clear_specific: List[str] - список ключів для очищення
        
        Returns:
            StateTransitionResult: результат переходу
        """
        try:
            # Отримуємо поточний стан та дані
            current_state = await state.get_state()
            current_data = await state.get_data() if preserve_data else {}
            
            # Очищаємо специфічні дані якщо потрібно
            if clear_specific:
                for key in clear_specific:
                    current_data.pop(key, None)
            
            # Додаємо нові дані
            if additional_data:
                current_data.update(additional_data)
            
            # Додаємо службову інформацію
            current_data.update({
                "last_transition": datetime.utcnow().isoformat(),
                "transition_type": transition_type.value
            })
            
            # Очищаємо стан якщо потрібно
            if not preserve_data and transition_type != TransitionType.ROLLBACK:
                await state.clear()
            
            # Встановлюємо новий стан
            await state.set_state(new_state)
            
            # Зберігаємо дані
            await state.set_data(current_data)
            
            # Зберігаємо в історію
            await self._save_to_history(current_state, str(new_state), current_data)
            
            # Формуємо результат
            result = StateTransitionResult(
                success=True,
                previous_state=current_state,
                new_state=str(new_state),
                timestamp=datetime.utcnow(),
                transition_type=transition_type,
                preserved_data=current_data
            )
            
            logger.info(f"State transition successful: {current_state} -> {new_state}")
            return result
            
        except Exception as e:
            error_msg = f"State transition failed: {str(e)}"
            logger.error(error_msg)
            return StateTransitionResult(
                success=False,
                previous_state=current_state,
                new_state=str(new_state),
                timestamp=datetime.utcnow(),
                transition_type=transition_type,
                preserved_data={},
                error=error_msg
            )

    async def rollback(self, state: FSMContext) -> StateTransitionResult:
        """Повернення до попереднього стану"""
        if not self.state_history:
            return StateTransitionResult(
                success=False,
                previous_state=await state.get_state(),
                new_state="",
                timestamp=datetime.utcnow(),
                transition_type=TransitionType.ROLLBACK,
                preserved_data={},
                error="No history available"
            )
            
        previous_state = self.state_history[-1]
        return await self.transition_state(
            state,
            MenuStates(previous_state["from_state"]),
            transition_type=TransitionType.ROLLBACK,
            additional_data=previous_state["data"]
        )
        
    async def reset_state(self, state: FSMContext) -> StateTransitionResult:
        """Повне скидання стану"""
        return await self.transition_state(
            state,
            MenuStates.MAIN_MENU,
            transition_type=TransitionType.RESET
        )

    def get_state_history(self) -> List[Dict[str, Any]]:
        """Отримати історію переходів"""
        return self.state_history

# Створюємо глобальний екземпляр менеджера станів
state_manager = StateManager()

# Приклад використання:
"""
@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    result = await state_manager.transition_state(
        state,
        MenuStates.MAIN_MENU,
        additional_data={"user_id": message.from_user.id}
    )
    
    if result.success:
        await message.answer("Ласкаво просимо до головного меню!")
    else:
        await message.answer("Виникла помилка. Спробуйте пізніше.")
        logger.error(f"Start handler error: {result.error}")
"""
