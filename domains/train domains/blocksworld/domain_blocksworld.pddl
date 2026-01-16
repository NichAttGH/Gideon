(define (domain blocksworld-4ops)
(:requirements :strips :typing :action-costs)
(:types block - object)
(:predicates (clear ?x - block)
             (on-table ?x - block)
             (arm-empty)
             (holding ?x - block)
             (on ?x - block ?y - block)
)

(:functions
	(total-cost) - number
)

(:action pickup
  :parameters (?ob - block)
  :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
  :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob)) 
               (not (arm-empty)) (increase (total-cost) 1)
               )
  )

(:action putdown
  :parameters  (?ob - block)
  :precondition (holding ?ob)
  :effect (and (clear ?ob) (arm-empty) (on-table ?ob) 
               (not (holding ?ob)) (increase (total-cost) 1)
               )
  )

(:action stack
  :parameters  (?ob - block ?underob - block)
  :precondition (and (clear ?underob) (holding ?ob))
  :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
               (not (clear ?underob)) (not (holding ?ob))
               (increase (total-cost) 1)
               )
  )

(:action unstack
  :parameters  (?ob - block ?underob - block)
  :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
  :effect (and (holding ?ob) (clear ?underob)
               (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty))
               (increase (total-cost) 1)
               )
  
  )
)