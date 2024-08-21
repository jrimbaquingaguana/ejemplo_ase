Feature: Captura de video en tiempo real

  Background:
    Given the application is running

  Scenario: Capturar video en tiempo real
    When I start real-time video capture
    Then the application should capture video in real-time
    When I stop real-time video capture
    Then the video should be saved successfully
