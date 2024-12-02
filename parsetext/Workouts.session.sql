Select 
    m.name as movement_name,
    sum(weight * reps) as total_weight_lifted, 
    count(distinct e.id) as total_sets,
    sum(reps) as total_reps,
    round(avg(reps), 1) as avg_reps_per_set,
    round(sum(weight*reps) / sum(reps), 1) as avg_weight_per_rep,
from exercise_set e
join movement m on e.movement_id = m.id
join workout w on e.workout_id = w.id
where w.date >= '2024-01-01'
group by 1
order by 2 desc;

