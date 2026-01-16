(define (domain maintenance)
 (:requirements :adl :typing :conditional-effects :action-costs)
 (:types plane day airport)
 (:predicates  (done ?p - plane)
  (today ?d - day)
  (at ?p - plane ?d - day ?c - airport)
  (next ?d - day ?d2 - day) )
 (:functions
   (total-cost) - number
 )

 (:action workat
  :parameters (?day - day ?airport - airport)
  :precondition (today ?day)
  :effect (and
     (not (today ?day))
     (forall (?plane - plane) (when (at ?plane ?day ?airport) (done ?plane)))
     (increase (total-cost) 1))
  )

)