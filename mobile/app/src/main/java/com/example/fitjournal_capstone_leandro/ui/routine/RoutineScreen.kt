package com.example.fitjournal_capstone_leandro.ui.routine

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.activity.compose.BackHandler
import androidx.navigation.NavHostController
import com.example.fitjournal_capstone_leandro.data.model.UserExercise
import com.example.fitjournal_capstone_leandro.navigation.Routes
import com.example.fitjournal_capstone_leandro.ui.theme.myCustomFont

private val AccentYellow = Color(0xFFFFEB3B)
private val BackgroundDark = Color(0xFF1B1B1E)
private val SurfaceDark = Color(0xFF2C2C2E)
private val TextGray = Color(0xFF8E8E93)

@Composable
fun RoutineScreen(viewModel: RoutineViewModel, navController: NavHostController) {
    val state by viewModel.state.collectAsState()

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundDark)
    ) {
        when (state.uiState) {
            is RoutineUiState.Loading -> {
                CircularProgressIndicator(
                    color = AccentYellow,
                    modifier = Modifier.align(Alignment.Center)
                )
            }

            is RoutineUiState.NoRoutine -> {
                NoRoutineContent(
                    onSelectDays = { viewModel.selectDaysPerWeek(it) }
                )
            }

            is RoutineUiState.Editing -> {
                EditingContent(
                    state = state,
                    muscleGroups = viewModel.muscleGroups,
                    onSelectDays = { viewModel.selectDaysPerWeek(it) },
                    onToggleMuscle = { day, muscle -> viewModel.toggleMuscleGroup(day, muscle) },
                    onOpenPicker = { day -> navController.navigate(Routes.exercisePicker(day)) },
                    onSave = { viewModel.saveRoutine() },
                    onCancel = { viewModel.cancelEditing() }
                )
            }

            is RoutineUiState.Success -> {
                ViewRoutineContent(
                    state = state,
                    onEdit = { viewModel.startEditing() }
                )
            }

            is RoutineUiState.Error -> {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = (state.uiState as RoutineUiState.Error).message,
                        color = Color(0xFFFF453A),
                        fontFamily = myCustomFont,
                        fontSize = 16.sp
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(
                        onClick = { viewModel.loadRoutine() },
                        colors = ButtonDefaults.buttonColors(containerColor = AccentYellow)
                    ) {
                        Text("Retry", color = Color.Black, fontFamily = myCustomFont)
                    }
                }
            }
        }

    }
}

// ─── NO ROUTINE ───────────────────────────────────────────────────────────────

@Composable
private fun NoRoutineContent(onSelectDays: (Int) -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Your Routine",
            fontSize = 32.sp,
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontFamily = myCustomFont
        )

        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = "How many days per week\ndo you want to train?",
            fontSize = 20.sp,
            color = Color.White,
            fontFamily = myCustomFont,
            textAlign = androidx.compose.ui.text.style.TextAlign.Center
        )

        Spacer(modifier = Modifier.height(32.dp))

        DaySelector(selectedDays = 0, onSelectDays = onSelectDays)
    }
}

// ─── EDITING ──────────────────────────────────────────────────────────────────

@Composable
private fun EditingContent(
    state: RoutineScreenState,
    muscleGroups: List<String>,
    onSelectDays: (Int) -> Unit,
    onToggleMuscle: (Int, String) -> Unit,
    onOpenPicker: (Int) -> Unit,
    onSave: () -> Unit,
    onCancel: () -> Unit
) {
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        item {
            Text(
                text = "Your Routine",
                fontSize = 32.sp,
                color = Color.White,
                fontWeight = FontWeight.Bold,
                fontFamily = myCustomFont
            )

            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "How many days per week\ndo you want to train?",
                fontSize = 18.sp,
                color = Color.White,
                fontFamily = myCustomFont,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )

            Spacer(modifier = Modifier.height(16.dp))

            DaySelector(
                selectedDays = state.selectedDays,
                onSelectDays = onSelectDays
            )

            Spacer(modifier = Modifier.height(32.dp))

            Text(
                text = "Select muscle groups for each day:",
                fontSize = 18.sp,
                color = Color.White,
                fontFamily = myCustomFont
            )

            Spacer(modifier = Modifier.height(16.dp))
        }

        // One card per day
        items((1..state.selectedDays).toList()) { day ->
            DayCard(
                day = day,
                muscleGroups = muscleGroups,
                daySelection = state.editingDays[day] ?: emptyMap(),
                onToggleMuscle = { muscle -> onToggleMuscle(day, muscle) },
                onOpenPicker = { onOpenPicker(day) }
            )
            Spacer(modifier = Modifier.height(16.dp))
        }

        item {
            Spacer(modifier = Modifier.height(8.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                OutlinedButton(
                    onClick = onCancel,
                    modifier = Modifier.padding(end = 12.dp)
                ) {
                    Text("Cancel", color = TextGray, fontFamily = myCustomFont)
                }
                Button(
                    onClick = onSave,
                    colors = ButtonDefaults.buttonColors(containerColor = AccentYellow)
                ) {
                    Text(
                        "Save Routine",
                        color = Color.Black,
                        fontFamily = myCustomFont,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

// ─── VIEW ROUTINE ─────────────────────────────────────────────────────────────

@Composable
private fun ViewRoutineContent(
    state: RoutineScreenState,
    onEdit: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "Your Routine",
            fontSize = 32.sp,
            color = Color.White,
            fontWeight = FontWeight.Bold,
            fontFamily = myCustomFont
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Training ${state.daysPerWeek} days per week",
            fontSize = 16.sp,
            color = TextGray,
            fontFamily = myCustomFont
        )

        Spacer(modifier = Modifier.height(24.dp))

        (1..state.daysPerWeek).forEach { day ->
            val muscles = state.routineDays[day.toString()] ?: emptyList()
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                verticalAlignment = Alignment.Top
            ) {
                Text(
                    text = "Day $day:",
                    fontSize = 16.sp,
                    color = AccentYellow,
                    fontWeight = FontWeight.Bold,
                    fontFamily = myCustomFont,
                    modifier = Modifier.width(60.dp)
                )
                Text(
                    text = if (muscles.isEmpty()) "Rest day" else muscles.joinToString(", "),
                    fontSize = 16.sp,
                    color = Color.White,
                    fontFamily = myCustomFont
                )
            }
            Divider(color = SurfaceDark)
        }

        Spacer(modifier = Modifier.height(32.dp))

        // The mobile editor only builds per_muscle routines for now. A routine
        // with manual days (created on the web) is view-only here so editing it
        // can't silently convert those days to per_muscle.
        if (state.isPerMuscleOnly) {
            Button(
                onClick = onEdit,
                colors = ButtonDefaults.buttonColors(containerColor = SurfaceDark)
            ) {
                Text("Edit Routine", color = Color.White, fontFamily = myCustomFont)
            }
        } else {
            Text(
                text = "This routine has manual days. Edit it on the web app for now.",
                color = TextGray,
                fontFamily = myCustomFont
            )
        }
    }
}

// ─── EXERCISE PICKER OVERLAY ──────────────────────────────────────────────────

@Composable
fun ExercisePickerScreen(
    viewModel: RoutineViewModel,
    day: Int,
    onDone: () -> Unit,
    onCancel: () -> Unit
) {
    val state by viewModel.state.collectAsState()
    val daySelection = state.editingDays[day] ?: emptyMap()
    val exercisesByMuscle = state.exercisesByMuscle

    // Snapshot on open so Cancel / system-back can revert this picker session.
    LaunchedEffect(day) { viewModel.beginPickerEdit(day) }
    BackHandler { onCancel() }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(BackgroundDark)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp)
        ) {
            Text(
                text = "Day $day — choose exercises",
                fontSize = 24.sp,
                color = Color.White,
                fontWeight = FontWeight.Bold,
                fontFamily = myCustomFont
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Tick the exercises to include, and set how many to draw each session.",
                fontSize = 13.sp,
                color = TextGray,
                fontFamily = myCustomFont
            )

            Spacer(modifier = Modifier.height(12.dp))

            LazyColumn(modifier = Modifier.weight(1f)) {
                if (daySelection.isEmpty()) {
                    item {
                        Text(
                            text = "No muscle groups selected for this day yet.",
                            color = TextGray,
                            fontFamily = myCustomFont,
                            fontSize = 14.sp
                        )
                    }
                }
                daySelection.forEach { (muscle, sel) ->
                    item(key = "hdr_$muscle") {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 14.dp, bottom = 4.dp)
                        ) {
                            Text(
                                text = muscle,
                                fontSize = 16.sp,
                                color = AccentYellow,
                                fontWeight = FontWeight.Bold,
                                fontFamily = myCustomFont,
                                modifier = Modifier.weight(1f)
                            )
                            Text(
                                text = "draw",
                                color = TextGray,
                                fontFamily = myCustomFont,
                                fontSize = 13.sp
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            StepperButton(label = "-") { viewModel.changeCount(day, muscle, -1) }
                            Text(
                                text = "${sel.count}",
                                color = Color.White,
                                fontFamily = myCustomFont,
                                fontSize = 16.sp,
                                modifier = Modifier.padding(horizontal = 12.dp)
                            )
                            StepperButton(label = "+") { viewModel.changeCount(day, muscle, 1) }
                        }
                    }

                    val exercises = exercisesByMuscle[muscle].orEmpty()
                    if (exercises.isEmpty()) {
                        item(key = "empty_$muscle") {
                            Text(
                                text = "No $muscle exercises in your library.",
                                color = TextGray,
                                fontFamily = myCustomFont,
                                fontSize = 13.sp,
                                modifier = Modifier.padding(vertical = 6.dp)
                            )
                        }
                    } else {
                        items(exercises, key = { "ex_${muscle}_${it.exercise_id}" }) { ex ->
                            val checked = sel.exerciseIds.contains(ex.exercise_id)
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { viewModel.toggleExercise(day, muscle, ex.exercise_id) }
                                    .padding(vertical = 6.dp)
                            ) {
                                CheckboxBox(checked = checked)
                                Spacer(modifier = Modifier.width(10.dp))
                                Text(
                                    text = ex.exercise_name,
                                    color = Color.White,
                                    fontFamily = myCustomFont,
                                    fontSize = 14.sp
                                )
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedButton(
                    onClick = onCancel,
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Cancel", color = TextGray, fontFamily = myCustomFont)
                }
                Button(
                    onClick = onDone,
                    colors = ButtonDefaults.buttonColors(containerColor = AccentYellow),
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Done", color = Color.Black, fontWeight = FontWeight.Bold, fontFamily = myCustomFont)
                }
            }
        }
    }
}

// ─── SHARED COMPOSABLES ───────────────────────────────────────────────────────

@Composable
private fun DaySelector(selectedDays: Int, onSelectDays: (Int) -> Unit) {
    Row(
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        (1..7).forEach { day ->
            val isSelected = day == selectedDays
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .border(
                        width = 2.dp,
                        color = if (isSelected) AccentYellow else Color.White,
                        shape = RoundedCornerShape(8.dp)
                    )
                    .background(
                        color = if (isSelected) AccentYellow.copy(alpha = 0.2f)
                        else Color.Transparent,
                        shape = RoundedCornerShape(8.dp)
                    )
                    .clickable { onSelectDays(day) },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "$day",
                    color = if (isSelected) AccentYellow else Color.White,
                    fontWeight = FontWeight.Bold,
                    fontFamily = myCustomFont,
                    fontSize = 18.sp
                )
            }
        }
    }
}

@Composable
private fun DayCard(
    day: Int,
    muscleGroups: List<String>,
    daySelection: Map<String, MuscleSelection>,
    onToggleMuscle: (String) -> Unit,
    onOpenPicker: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(SurfaceDark, RoundedCornerShape(12.dp))
            .padding(16.dp)
    ) {
        Text(
            text = "Day $day",
            fontSize = 18.sp,
            color = AccentYellow,
            fontWeight = FontWeight.Bold,
            fontFamily = myCustomFont
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Muscle group toggle buttons — wrap in rows of 3
        val rows = muscleGroups.chunked(3)
        rows.forEach { rowMuscles ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                rowMuscles.forEach { muscle ->
                    val isSelected = daySelection.containsKey(muscle)
                    OutlinedButton(
                        onClick = { onToggleMuscle(muscle) },
                        modifier = Modifier
                            .weight(1f)
                            .height(40.dp),
                        colors = ButtonDefaults.outlinedButtonColors(
                            containerColor = if (isSelected) AccentYellow.copy(alpha = 0.2f)
                            else Color.Transparent
                        ),
                        border = BorderStroke(
                            width = 1.5.dp,
                            color = if (isSelected) AccentYellow else Color.Gray
                        ),
                        contentPadding = PaddingValues(4.dp)
                    ) {
                        Text(
                            text = muscle,
                            color = if (isSelected) AccentYellow else Color.White,
                            fontFamily = myCustomFont,
                            fontSize = 11.sp
                        )
                    }
                }
                // Fill empty slots in last row
                repeat(3 - rowMuscles.size) {
                    Spacer(modifier = Modifier.weight(1f))
                }
            }
            Spacer(modifier = Modifier.height(8.dp))
        }

        // Choose-exercises — a plain left-aligned text link (secondary action,
        // deliberately quieter than the muscle toggle pills above).
        if (daySelection.isNotEmpty()) {
            val totalSelected = daySelection.values.sumOf { it.exerciseIds.size }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Choose exercises ($totalSelected selected) ›",
                color = AccentYellow,
                fontFamily = myCustomFont,
                fontSize = 14.sp,
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { onOpenPicker() }
                    .padding(vertical = 4.dp)
            )
        }
    }
}

@Composable
private fun StepperButton(label: String, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(28.dp)
            .border(1.dp, Color.Gray, RoundedCornerShape(6.dp))
            .clickable { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Text(label, color = Color.White, fontFamily = myCustomFont, fontSize = 18.sp)
    }
}

@Composable
private fun CheckboxBox(checked: Boolean) {
    Box(
        modifier = Modifier
            .size(20.dp)
            .border(
                width = 1.5.dp,
                color = if (checked) AccentYellow else Color.Gray,
                shape = RoundedCornerShape(4.dp)
            )
            .background(
                color = if (checked) AccentYellow else Color.Transparent,
                shape = RoundedCornerShape(4.dp)
            ),
        contentAlignment = Alignment.Center
    ) {
        if (checked) {
            Text("✓", color = Color.Black, fontSize = 13.sp, fontWeight = FontWeight.Bold)
        }
    }
}