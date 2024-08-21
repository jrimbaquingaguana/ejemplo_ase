Feature: Realizar clics con el ojo izquierdo

  Background:
    Given the application is running

  Scenario: Realizar clic con el ojo izquierdo
    When I blink my left eye
    Then the application should register a mouse click
