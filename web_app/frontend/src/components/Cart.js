import React, { useEffect, useState } from "react";
import userService from "../services/userService";
import { useParams, useNavigate } from "react-router-dom";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  const { user_id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await userService.getCart(user_id);
      console.log(response.cart); // Debugging the response
      if (response.cart && response.cart.length > 0) {
        setCartItems(response.cart[0].items); // Accessing the items array inside cart
      } else {
        setCartItems([]);
      }
    } catch (err) {
      console.error("Error fetching cart:", err);
      setError("Failed to load cart items. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (itemId) => {
    try {
      await userService.removeFromCart(user_id, itemId);
      setCartItems(cartItems.filter((item) => item.item_id !== itemId));
    } catch (err) {
      console.error("Error removing item:", err);
      setError("Failed to remove item from cart. Please try again.");
    }
  };

  const handleCheckout = async () => {
    setCheckoutLoading(true);
    setError(null);
    try {
      const response = await userService.checkout(user_id, cartItems);
      if (response.success) {
        // Redirect to confirmation page or payment gateway
        alert("Checkout successful!");
        navigate("/order-confirmation"); // Adjust with your route for confirmation
      } else {
        setError("Checkout failed. Please try again.");
      }
    } catch (err) {
      console.error("Error during checkout:", err);
      setError("An error occurred during checkout. Please try again.");
    } finally {
      setCheckoutLoading(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="cart-container">
      <h1>Your Cart</h1>
      {error && <div className="error-message">{error}</div>}
      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <table border="1" cellPadding="8" cellSpacing="0">
          <thead>
            <tr>
              <th>#</th>
              <th>Item Description</th>
              <th>Category</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {cartItems.map((item, index) => (
              <tr key={item.item_id}>
                <td>{index + 1}</td>
                <td>{item.description || "N/A"}</td>
                <td>{item.category || "N/A"}</td>
                <td>${item.starting_price?.toFixed(2) || "0.00"}</td>
                <td>{item.quantity || 1}</td>
                <td>
                  <button onClick={() => handleRemove(item.item_id)}>
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Checkout Button */}
      {cartItems.length > 0 && (
        <div className="checkout-section">
          {checkoutLoading ? (
            <div>Processing Checkout...</div>
          ) : (
            <button onClick={handleCheckout}>Proceed to Checkout</button>
          )}
        </div>
      )}
    </div>
  );
};

export default Cart;
