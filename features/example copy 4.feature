Feature: Control del cursor del mouse con el ojo derecho

  Background:
    Given the application is running

  Scenario: Controlar el cursor del mouse con el ojo derecho
    When I move my right eye
    Then the cursor should move accordingly on the screen
