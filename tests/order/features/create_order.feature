Feature: Create order
  As a shipper
  I want to create orders via order-create
  So that parcels can be shipped

  Background:
    Given I am authenticated as a shipper

  @create_order_success
  Scenario: Success order create
    Given a create order payload with:
      | field           | value    |
      | service_type    | Parcel   |
      | service_level   | Standard |
      | from_data       | Random   |
      | to_data         | index-1  |
      | number_of_order | 3        |
    When I create the order(s)
    Then each order response status should be 200 or 201
    And I store the tracking number(s)
