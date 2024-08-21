Feature: Control del cursor del mouse con el ojo derecho

  Background:
    Given the application is running

  Scenario: Controlar el cursor del mouse usando el ojo derecho
    When I start eye tracking with right eye control
    Then the application should move the cursor with the right eye movement
    When I stop eye tracking with right eye control
    Then the cursor control by the right eye should stop
