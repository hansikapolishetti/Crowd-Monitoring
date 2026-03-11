import React from "react";

function Login() {

  return (
    <div className="h-screen flex items-center justify-center bg-gray-900">

      <div className="bg-gray-800 p-8 rounded-lg w-80">

        <h2 className="text-white text-2xl mb-6 text-center">
          Crowd Monitoring Login
        </h2>

        <input
          className="w-full p-2 mb-4 rounded"
          type="text"
          placeholder="Username"
        />

        <input
          className="w-full p-2 mb-4 rounded"
          type="password"
          placeholder="Password"
        />

        <button className="w-full bg-green-500 p-2 rounded text-white">
          Login
        </button>

      </div>

    </div>

  );

}

export default Login;