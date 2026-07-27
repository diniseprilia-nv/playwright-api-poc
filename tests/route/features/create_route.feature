Feature: Create route
  As an operator
  I want to create a route via route-v2
  So that a driver can be assigned for today's deliveries

  Background:
    Given I am authenticated as an operator

  @create_route_today
  Scenario: Create route with today date and country config
    Given a create route payload for today using country config
    When I create a route
    Then the response status should be 200 or 201
    And the payload date should be today
    And the payload should use country driver hub and zone ids
    And the response body should not be empty

  @create_route_country_ids
  Scenario: Create route payload uses country driver hub and zone
    Given a create route payload for today using country config
    And country config has valid driver hub and zone ids
    When I create a route
    Then the response status should be 200 or 201
    And the payload should use country driver hub and zone ids

  @create_route_identity
  Scenario: Create route response includes route identity
    Given a create route payload for today using country config
    When I create a route
    Then the response status should be 200 or 201
    And the response should include a route identity

  @create_route_missing_driver
  Scenario: Create route rejects missing driver id
    Given a create route payload for today using country config
    And the payload is missing "driver_id"
    When I create a route
    Then the response status should be 400 or 422

  @create_route_invalid_driver
  Scenario: Create route rejects invalid driver id
    Given a create route payload for today using country config
    And the payload driver_id is set to -1
    When I create a route
    Then the response status should be 400 or 404 or 422
