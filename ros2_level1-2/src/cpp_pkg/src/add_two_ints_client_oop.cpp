#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class AddTwoIntsClientNode : public rclcpp::Node
{

public:
    AddTwoIntsClientNode() : Node("add_two_ints_client")
    {
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
    }

    void call_add_two_ints(int a, int b)
    {
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;

        auto result_future = client_->async_send_request(request);

        if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), result_future) ==
            rclcpp::FutureReturnCode::SUCCESS)
        {
            RCLCPP_INFO(this->get_logger(), "Result of add_two_ints: %d", result_future.get()->sum);
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Failed to call service add_two_ints");
        }
    }

private:
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};

int main(int args, char **argv)
{

    rclcpp::init(args, argv);
    auto node = std::make_shared<AddTwoIntsClientNode>();
    node->call_add_two_ints(10, 20);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}