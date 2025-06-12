;; source: https://github.com/AI-Planning/pddl-generators/blob/main/sokoban/domain.pddl
;; updates:
;;   - only focus on microban instances, hence 4 constant directions
;;
(define (domain sokoban)
(:requirements :typing :action-costs)
(:types location box)

(:predicates
             (at-robot ?l - location)
             (at ?o - box ?l - location)
             (adjacent ?l1 - location ?l2 - location) 
             (clear ?l - location)
)

(:functions
    (total-cost) - number
)

(:action move
:parameters (?from - location ?to - location)
:precondition (and (clear ?to) (at-robot ?from) (adjacent ?from ?to))
:effect (and (at-robot ?to) (not (at-robot ?from)) (increase (total-cost) 1))
)
             

(:action push
:parameters  (?rloc - location ?bloc - location ?floc - location ?b - box)
:precondition (and (at-robot ?rloc) (at ?b ?bloc) (clear ?floc)
	           (adjacent ?rloc ?bloc) (adjacent ?bloc ?floc))

:effect (and (at-robot ?bloc) (at ?b ?floc) (clear ?bloc)
             (not (at-robot ?rloc)) (not (at ?b ?bloc)) (not (clear ?floc)) (increase (total-cost) 1))
)
)