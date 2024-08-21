Feature: Recording and Detection Operations

  Scenario: Start recording and detection
    Given the application is running
    When I start recording
    And I start detection
    Then I stop recording
    And I stop detection
