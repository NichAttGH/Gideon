(define (domain blocks_world)
    (:requirements :strips :typing)
    
    (:types
        block
    )

    (:predicates
        (on ?x - block ?y - block)         ; il blocco x è sopra il blocco y
        (ontable ?x - block)               ; il blocco x è sul tavolo
        (clear ?x - block)                 ; il blocco x è libero
        (holding ?x - block)               ; il blocco x è in mano
        (handempty)                        ; la mano è vuota
    )

    (:action pick-up
        :parameters (?x - block)
        :precondition (and (ontable ?x) (clear ?x) (handempty))
        :effect (and (holding ?x)
                     (not (ontable ?x))
                     (not (clear ?x))
                     (not (handempty)))
    )

    (:action put-down
        :parameters (?x - block)
        :precondition (holding ?x)
        :effect (and (ontable ?x)
                     (clear ?x)
                     (handempty)
                     (not (holding ?x)))
    )

    (:action stack
        :parameters (?x - block ?y - block)
        :precondition (and (holding ?x) (clear ?y))
        :effect (and (on ?x ?y)
                     (clear ?x)
                     (handempty)
                     (not (holding ?x))
                     (not (clear ?y)))
    )

    (:action unstack
        :parameters (?x - block ?y - block)
        :precondition (and (on ?x ?y) (clear ?x) (handempty))
        :effect (and (holding ?x)
                     (clear ?y)
                     (not (on ?x ?y))
                     (not (clear ?x))
                     (not (handempty)))
    )
)