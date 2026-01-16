(define (domain briefcase)
(:requirements :typing :negative-preconditions :conditional-effects :action-costs)
(:types portable location)
(:predicates (at ?y - portable ?x - location)
             (in ?x - portable)
             (is-at ?x - location))

(:functions
  (total-cost) - number
)

(:action move
  :parameters (?m ?l - location)
  :precondition  (is-at ?m)
  :effect (and (is-at ?l) (not (is-at ?m))
		    (forall (?x - portable) (when (in ?x)
		      (and (at ?x ?l) (not (at ?x ?m)))))
		    (increase (total-cost) 1)
  )
)

(:action take-out
      :parameters (?x - portable)
      :precondition (in ?x)
      :effect (and (not (in ?x)) (increase (total-cost) 1))
)
      
(:action put-in
      :parameters (?x - portable ?l - location)
      :precondition (and (not (in ?x)) (at ?x ?l) (is-at ?l))
      :effect (and (in ?x) (increase (total-cost) 1))
)
)