Feature: Superposición de puntos de referencia faciales

  Background:
    Given the application is running

  Scenario: Superponer puntos de referencia faciales en el video
    When I start face detection with landmarks
    Then the application should overlay facial landmarks on detected faces
    When I stop face detection with landmarks
    Then the facial landmarks overlay should stop
