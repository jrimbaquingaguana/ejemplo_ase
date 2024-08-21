Feature: Interfaz gráfica de usuario con botones Iniciar Detección, Iniciar Grabación, Salir
  As a user
  I want to have a graphical user interface with buttons for key actions
  So that I can interact with the system easily

  Scenario: Display of the user interface with the necessary buttons
    Given the application is running
    Then I should see the buttons "Iniciar Detección", "Iniciar Grabación", and "Salir"
    And I attempt to perform an action that will fail