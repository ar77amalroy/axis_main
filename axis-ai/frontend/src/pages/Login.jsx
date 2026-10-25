import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import api from "../api";

export default function Login() {
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse) => {
    setError("");
    try {
      const { data } = await api.post("/auth/google", {
        credential: credentialResponse.credential,
      });
      localStorage.setItem("token", data.access_token);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Google sign-in failed");
    }
  };

  const handleError = () => {
    setError("Google sign-in failed. Please try again.");
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>AXIS AI</h1>
        <p className="subtitle">Sign in to your workspace</p>
        {error && <div className="error">{error}</div>}
        <div className="google-btn-container">
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={handleError}
            theme="filled_black"
            shape="rectangular"
          />
        </div>
      </div>
    </div>
  );
}
