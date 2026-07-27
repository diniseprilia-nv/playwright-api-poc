Feature: Archive route
  As an operator
  I want to archive a route via route-v2
  So that an unused or completed route can be closed

  Background:
    Given I am authenticated as an operator

  @archive_route
  Scenario: Archive a newly created route
    Given a create route payload for today using country config
    When I create a route
    Then the response status should be 200 or 201
    And I store the created route id
    When I archive the stored route
    Then the response status should be 200 or 204

  @archive_route_invalid_id
  Scenario: Archive route rejects invalid route id
    Given the route id is set to 999999999
    When I archive the stored route
    Then the response status should be 400 or 404 or 422
