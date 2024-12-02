(define (domain moving_objects)
  (:requirements :strips :typing :fluents :existential-preconditions)

  ;; Tipi di oggetti
  (:types 
    room obj - object
  )

  ;; Predicati
  (:predicates
    (in ?o - object ?r - room)       ;; Oggetto si trova in una stanza
    (at ?r - room)                   ;; La stanza è disponibile
    (clear ?o - object)              ;; Oggetto è libero (non sopra un altro oggetto)
  )

  ;; Funzioni (fluents)
  (:functions
    (distance ?r1 - room ?r2 - room) - number ;; Distanza tra due stanze
  )

  ;; Azioni
  ;; L'azione di spostamento di un oggetto
  (:action move
    :parameters (?o - object ?from - room ?to - room)  ;; Oggetto e stanze di origine e destinazione
    :precondition (and 
      (in ?o ?from)    ;; L'oggetto deve essere nella stanza di origine
      (clear ?o)       ;; L'oggetto deve essere libero da altri oggetti
      (at ?from)       ;; La stanza di origine deve essere disponibile
      (at ?to)         ;; La stanza di destinazione deve essere disponibile
    )
    :effect (and
      (not (in ?o ?from))  ;; L'oggetto non è più nella stanza di origine
      (in ?o ?to)          ;; L'oggetto ora è nella stanza di destinazione
    )
  )

  ;; Azione per rendere un oggetto "clear", se non è sopra un altro oggetto
  (:action clear-object
    :parameters (?o - object ?r - room)
    :precondition (and
      (in ?o ?r)          ;; L'oggetto deve essere nella stanza
      (not (exists (?o2 - object) (in ?o2 ?r))) ;; Niente altri oggetti sopra
    )
    :effect (clear ?o)   ;; Ora l'oggetto è libero
  )
)
