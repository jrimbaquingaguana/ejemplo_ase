Feature: Detección automática de rostros en el video

  Background:
    Given the application is running

  Scenario: Detectar rostros automáticamente en el video
    When I start face detection
    Then the application should detect faces in the video feed
    When I stop face detection
    Then the face detection should stop
