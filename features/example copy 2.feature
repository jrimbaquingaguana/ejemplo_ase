Feature: Interfaz gráfica de usuario con botones Iniciar Detección, Iniciar Grabación, Salir

  Background:
    Given the application is running

  Scenario: Iniciar y detener la detección y grabación
    When I start detection
    Then the application should start detecting faces

    When I start recording
    Then the application should start recording

    When I stop detection
    Then the application should stop detecting faces

    When I stop recording
    Then the application should stop recording
