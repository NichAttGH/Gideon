(define (problem BW-rand-4)
    (:domain blocksworld-4ops)
    (:requirements :typing :action-costs)
    (:objects b1 b2 b3 b4 )
    (:init
        (= (total-cost) 0)
        (arm-empty)
        (on b1 b4)
        (on b2 b3)
        (on b3 b1)
        (on-table b4)
        (clear b2)
    )
    (:goal
    (and
        (on b3 b2))
    )
    (:metric minimize (total-cost))
)