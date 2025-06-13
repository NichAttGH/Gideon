(define (problem floor-tile_problem_000001)
    (:domain floor-tile)
    (:requirements :action-costs :typing)
    (:objects
    c0 c1 - color
    r0 r1 - robot
    tile_0-0 tile_0-1 tile_0-2 tile_1-0 tile_1-1 tile_1-2 tile_2-0 tile_2-1 tile_2-2 - tile)
    (:init (= (total-cost) 0.0) (available-color c0) (available-color c1) (clear tile_0-0) (clear tile_0-1) (clear tile_1-1) (clear tile_1-2) (clear tile_2-0) (clear tile_2-1) (clear tile_2-2) (down tile_0-0 tile_1-0) (down tile_0-1 tile_1-1) (down tile_0-2 tile_1-2) (down tile_1-0 tile_2-0) (down tile_1-1 tile_2-1) (down tile_1-2 tile_2-2) (left tile_0-0 tile_0-1) (left tile_0-1 tile_0-2) (left tile_1-0 tile_1-1) (left tile_1-1 tile_1-2) (left tile_2-0 tile_2-1) (left tile_2-1 tile_2-2) (right tile_0-1 tile_0-0) (right tile_0-2 tile_0-1) (right tile_1-1 tile_1-0) (right tile_1-2 tile_1-1) (right tile_2-1 tile_2-0) (right tile_2-2 tile_2-1) (robot-at r0 tile_1-0) (robot-at r1 tile_0-2) (robot-has r0 c0) (robot-has r1 c1) (up tile_1-0 tile_0-0) (up tile_1-1 tile_0-1) (up tile_1-2 tile_0-2) (up tile_2-0 tile_1-0) (up tile_2-1 tile_1-1) (up tile_2-2 tile_1-2))
    (:goal (and (painted tile_1-0 c1) (painted tile_0-1 c1) (painted tile_1-1 c0) (painted tile_0-2 c0) (painted tile_0-0 c1) (painted tile_2-2 c0)))
    (:metric minimize (total-cost))
)