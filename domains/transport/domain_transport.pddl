; source: https://github.com/AI-Planning/pddl-generators/blob/main/transport/domain.pddl
; updates:
;  - removed :action-costs and :functions
;  - capacity type now is size
;  - capacity-number predicate now is capacity
(define (domain transport)
  (:requirements :typing :action-costs)
  (:types
        size location vehicle package - object
  )

  (:predicates
     (road ?l1 ?l2 - location)
     (atv ?x - vehicle ?v - location)
     (atp ?x - package ?v - location)
     (in ?x - package ?v - vehicle)
     (capacity ?v - vehicle ?s1 - size)
     (capacity-predecessor ?s1 ?s2 - size)
  )

  (:functions
    (total-cost) - number
  )

  (:action drive
    :parameters (?v - vehicle ?l1 ?l2 - location)
    :precondition (and
        (atv ?v ?l1)
        (road ?l1 ?l2)
      )
    :effect (and
        (not (atv ?v ?l1))
        (atv ?v ?l2)
        (increase (total-cost) 1)
      )
  )

 (:action pick-up
    :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - size)
    :precondition (and
        (atv ?v ?l)
        (atp ?p ?l)
        (capacity-predecessor ?s1 ?s2)
        (capacity ?v ?s2)
      )
    :effect (and
        (not (atp ?p ?l))
        (in ?p ?v)
        (capacity ?v ?s1)
        (not (capacity ?v ?s2))
        (increase (total-cost) 1)
      )
  )

  (:action drop
    :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - size)
    :precondition (and
        (atv ?v ?l)
        (in ?p ?v)
        (capacity-predecessor ?s1 ?s2)
        (capacity ?v ?s1)
      )
    :effect (and
        (not (in ?p ?v))
        (atp ?p ?l)
        (capacity ?v ?s2)
        (not (capacity ?v ?s1))
        (increase (total-cost) 1)
      )
  )

)