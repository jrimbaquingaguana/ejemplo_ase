Feature: Keywords and Data-Driven Testing

  Scenario Outline: Perform detection and recording operations
    Given the application is running
    When I perform "<action>" with "<operation>"
    Then the application should "<expected_result>"

    Examples:
      | action         | operation         | expected_result                           |
      | start          | detection         | start detecting faces                     |
      | start          | recording         | start recording                            |
      | stop           | detection         | stop detecting faces                      |
      | stop           | recording         | stop recording                             |
