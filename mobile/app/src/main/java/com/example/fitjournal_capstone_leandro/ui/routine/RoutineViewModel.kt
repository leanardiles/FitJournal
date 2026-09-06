package com.example.fitjournal_capstone_leandro.ui.routine

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.fitjournal_capstone_leandro.analytics.AnalyticsLogger
import com.example.fitjournal_capstone_leandro.data.model.MusclePool
import com.example.fitjournal_capstone_leandro.data.model.TrainingDayResponse
import com.example.fitjournal_capstone_leandro.data.model.UserExercise
import com.example.fitjournal_capstone_leandro.data.repository.IUserRoutineRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

sealed class RoutineUiState {
    object Loading : RoutineUiState()
    object NoRoutine : RoutineUiState()
    object Editing : RoutineUiState()
    object Success : RoutineUiState()
    data class Error(val message: String) : RoutineUiState()
}

/**
 * A muscle's selection within a day being edited: which exercises are in the
 * pool, and how many to draw per session.
 */
data class MuscleSelection(
    val exerciseIds: Set<Int> = emptySet(),
    val count: Int = 3
)

data class RoutineScreenState(
    val uiState: RoutineUiState = RoutineUiState.Loading,
    val daysPerWeek: Int = 0,
    val selectedDays: Int = 0,                                   // days selected in editor
    val routineDays: Map<String, List<String>> = emptyMap(),    // existing routine (view mode display)
    val editingDays: Map<Int, Map<String, MuscleSelection>> = emptyMap(),  // day -> muscle -> selection
    val exercisesByMuscle: Map<String, List<UserExercise>> = emptyMap(),   // library, for the picker
    val pickerDay: Int? = null,                                 // which day's exercise picker is open
    val isPerMuscleOnly: Boolean = true,                        // false if any day is manual (web-made)
    val savedMessage: String? = null
)

class RoutineViewModel(
    private val repository: IUserRoutineRepository
) : ViewModel() {

    private val _state = MutableStateFlow(RoutineScreenState())
    val state: StateFlow<RoutineScreenState> = _state.asStateFlow()

    // Raw routine days from the last load — used to prefill the editor (pool + counts).
    private var rawDays: List<TrainingDayResponse> = emptyList()

    val muscleGroups = listOf(
        "Legs", "Shoulders", "Chest", "Glutes",
        "Biceps", "Triceps", "Back", "Calves", "Abs"
    )

    init {
        loadRoutine()
    }

    fun loadRoutine() {
        viewModelScope.launch {
            _state.value = _state.value.copy(uiState = RoutineUiState.Loading)

            // Library for the exercise picker (grouped by muscle).
            val exByMuscle = repository.getExercises().getOrNull().orEmpty()
                .groupBy { it.exercise_muscle_group }

            val result = repository.getRoutine()
            if (result.isSuccess) {
                val routine = result.getOrNull()!!
                rawDays = routine.days
                if (routine.days_per_week == 0 || routine.days.isEmpty()) {
                    _state.value = _state.value.copy(
                        uiState = RoutineUiState.NoRoutine,
                        exercisesByMuscle = exByMuscle
                    )
                } else {
                    val displayMap = routine.days
                        .sortedBy { it.day_number }
                        .associate { it.day_number.toString() to musclesForDisplay(it) }
                    _state.value = _state.value.copy(
                        uiState = RoutineUiState.Success,
                        daysPerWeek = routine.days_per_week,
                        routineDays = displayMap,
                        exercisesByMuscle = exByMuscle,
                        isPerMuscleOnly = routine.days.all { it.day_type == "per_muscle" }
                    )
                }
            } else {
                _state.value = _state.value.copy(
                    uiState = RoutineUiState.Error(
                        result.exceptionOrNull()?.message ?: "Failed to load routine"
                    )
                )
            }
        }
    }

    private fun musclesForDisplay(day: TrainingDayResponse): List<String> =
        if (day.day_type == "manual") {
            day.exercises.map { it.muscle_group }.distinct()
        } else {
            day.muscles.map { it.muscle_group }
        }

    /**
     * User selected number of training days — move to editing mode.
     * Existing days' content is preserved when the count changes.
     */
    fun selectDaysPerWeek(days: Int) {
        val existing = _state.value.editingDays
        val editing = (1..days).associateWith { existing[it] ?: emptyMap() }
        _state.value = _state.value.copy(
            uiState = RoutineUiState.Editing,
            selectedDays = days,
            editingDays = editing
        )
    }

    /**
     * Toggle a muscle group for a day. Selecting a muscle defaults its pool to
     * ALL of that muscle's exercises (curate by unchecking in the picker).
     */
    fun toggleMuscleGroup(day: Int, muscle: String) {
        val current = _state.value.editingDays.toMutableMap()
        val dayMap = (current[day] ?: emptyMap()).toMutableMap()
        if (dayMap.containsKey(muscle)) {
            dayMap.remove(muscle)
        } else {
            val allIds = _state.value.exercisesByMuscle[muscle].orEmpty()
                .map { it.exercise_id }.toSet()
            val count = if (allIds.isEmpty()) 1 else minOf(3, allIds.size)
            dayMap[muscle] = MuscleSelection(exerciseIds = allIds, count = count)
        }
        current[day] = dayMap
        _state.value = _state.value.copy(editingDays = current)
    }

    // ---- Exercise picker ----

    fun openExercisePicker(day: Int) {
        _state.value = _state.value.copy(pickerDay = day)
    }

    fun closeExercisePicker() {
        _state.value = _state.value.copy(pickerDay = null)
    }

    fun toggleExercise(day: Int, muscle: String, exerciseId: Int) {
        val current = _state.value.editingDays.toMutableMap()
        val dayMap = (current[day] ?: return).toMutableMap()
        val sel = dayMap[muscle] ?: return
        val ids = sel.exerciseIds.toMutableSet()
        if (ids.contains(exerciseId)) ids.remove(exerciseId) else ids.add(exerciseId)
        // Keep count within the new pool size (cap at selected, floor 1).
        val newCount = if (ids.isEmpty()) 1 else minOf(sel.count, ids.size).coerceAtLeast(1)
        dayMap[muscle] = sel.copy(exerciseIds = ids, count = newCount)
        current[day] = dayMap
        _state.value = _state.value.copy(editingDays = current)
    }

    /** Nudge a muscle's per-session count by delta, clamped to [1, poolSize]. */
    fun changeCount(day: Int, muscle: String, delta: Int) {
        val current = _state.value.editingDays.toMutableMap()
        val dayMap = (current[day] ?: return).toMutableMap()
        val sel = dayMap[muscle] ?: return
        val maxCount = maxOf(1, sel.exerciseIds.size)
        val newCount = (sel.count + delta).coerceIn(1, maxCount)
        dayMap[muscle] = sel.copy(count = newCount)
        current[day] = dayMap
        _state.value = _state.value.copy(editingDays = current)
    }

    fun saveRoutine() {
        viewModelScope.launch {
            val editingDays = _state.value.editingDays

            if (editingDays.values.all { it.isEmpty() }) {
                _state.value = _state.value.copy(
                    uiState = RoutineUiState.Error("Please select at least one muscle group")
                )
                return@launch
            }

            // Every day needs >=1 muscle, and every muscle needs >=1 exercise in its pool.
            for ((day, muscleMap) in editingDays.toSortedMap()) {
                if (muscleMap.isEmpty()) {
                    _state.value = _state.value.copy(
                        uiState = RoutineUiState.Error("Day $day needs at least one muscle group")
                    )
                    return@launch
                }
                for ((muscle, sel) in muscleMap) {
                    if (sel.exerciseIds.isEmpty()) {
                        _state.value = _state.value.copy(
                            uiState = RoutineUiState.Error("Day $day: pick at least one $muscle exercise")
                        )
                        return@launch
                    }
                }
            }

            val days: Map<Int, List<MusclePool>> = editingDays.mapValues { (_, muscleMap) ->
                muscleMap.map { (muscle, sel) ->
                    MusclePool(
                        muscle_group = muscle,
                        exercise_ids = sel.exerciseIds.toList(),
                        exercise_count = sel.count
                    )
                }
            }

            val result = repository.saveRoutine(days)
            if (result.isSuccess) {
                AnalyticsLogger.logRoutineSaved(_state.value.selectedDays)
                loadRoutine()
            } else {
                _state.value = _state.value.copy(
                    uiState = RoutineUiState.Error(
                        result.exceptionOrNull()?.message ?: "Failed to save routine"
                    )
                )
            }
        }
    }

    /**
     * Switch to editing an existing routine — prefill each day's muscles with
     * their saved pool (checked exercises) and per-muscle count.
     */
    fun startEditing() {
        val editing = rawDays.sortedBy { it.day_number }.associate { day ->
            val muscleMap = day.muscles.associate { m ->
                val ids = day.exercises
                    .filter { it.muscle_group == m.muscle_group }
                    .map { it.exercise_id }
                    .toSet()
                m.muscle_group to MuscleSelection(exerciseIds = ids, count = m.exercise_count)
            }
            day.day_number to muscleMap
        }
        _state.value = _state.value.copy(
            uiState = RoutineUiState.Editing,
            selectedDays = _state.value.daysPerWeek,
            editingDays = editing
        )
    }

    fun cancelEditing() {
        if (_state.value.daysPerWeek > 0) {
            _state.value = _state.value.copy(uiState = RoutineUiState.Success, pickerDay = null)
        } else {
            _state.value = _state.value.copy(uiState = RoutineUiState.NoRoutine, pickerDay = null)
        }
    }
}

class RoutineViewModelFactory(
    private val repository: IUserRoutineRepository
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(RoutineViewModel::class.java)) {
            return RoutineViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}