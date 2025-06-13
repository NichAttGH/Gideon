; source => https://github.com/AI-Planning/pddl-generators/blob/main/spanner/domain.pddl
(define (domain spanner)
(:requirements :typing :strips :action-costs)
(:types
	location man nut spanner - object
)

(:predicates
	(atm ?m - man ?l - location)
	(atn ?n - nut ?l - location)
	(ats ?s - spanner ?l - location)
	(carrying ?m - man ?s - spanner)
	(usable ?s - spanner)
	(link ?l1 - location ?l2 - location)
	(tightened ?n - nut)
	(loose ?n - nut))

(:functions
        (total-cost) - number
)

(:action walk
        :parameters (?start - location ?end - location ?m - man)
        :precondition (and (atm ?m ?start)
                           (link ?start ?end))
        :effect (and (not (atm ?m ?start)) (atm ?m ?end)
        (increase (total-cost) 1)
        ))

(:action pickup_spanner
        :parameters (?l - location ?s - spanner ?m - man)
        :precondition (and (atm ?m ?l)
                           (ats ?s ?l))
        :effect (and (not (ats ?s ?l))
                     (carrying ?m ?s)
                     (increase (total-cost) 1)
                     ))

(:action tighten_nut
        :parameters (?l - location ?s - spanner ?m - man ?n - nut)
        :precondition (and (atm ?m ?l)
		      	   (atn ?n ?l)
			   (carrying ?m ?s)
			   (usable ?s)
			   (loose ?n))
        :effect (and (not (loose ?n))(not (usable ?s)) (tightened ?n)
        (increase (total-cost) 1)
        ))
)