SELECT
    e.name AS exercise_name
FROM
    exercise_set es
    JOIN movement e ON es.movement_id = e.id
    JOIN equipment_set eseq ON es.id = eseq.set_id
    JOIN equipment eq ON eseq.equipment_id = eq.id
    JOIN position_set es_p ON es.id = es_p.set_id
    JOIN position p ON es_p.position_id = p.id
    JOIN movement_muscle_group mmg ON e.id = mmg.movement_id
    JOIN muscle_group mg ON mmg.muscle_group_id = mg.id
WHERE
    1 = 1
    --AND eq.name in ('Barbell', 'Dumbbell', 'Kettlebell', 'Machine', 'Cable', 'Bodyweight')
    --AND p.name in ('Standing', 'Seated', 'Kneeling', 'Lying')
    --AND mg.name in ('Chest', 'Back', 'Shoulders', 'Legs', 'Arms')
GROUP BY
    e.name
ORDER BY
    max(es.weight) DESC;