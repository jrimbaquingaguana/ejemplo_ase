Feature: Interfaz gráfica de usuario con botones Iniciar Detección, Iniciar Grabación, Salir

  As a user
  I want to have a graphical user interface with buttons for key actions
  So that I can interact with the system easily

  Scenario: Display of the user interface with the necessary buttons
    Given the application is running
    When I attempt to start video capture with an intentional error
    Then a report with screenshots and video should be generated
