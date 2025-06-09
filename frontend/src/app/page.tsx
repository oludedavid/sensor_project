"use client";
import ImageTransition from "@/components/imageTransition";
import { useEffect, useState } from "react";
import { useAuth } from "@/context/authContext";
import useApiRequest from "@/hooks/usefectchData";
import lodash from "lodash";
import { setCookie } from "cookies-next";
import { useRouter } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

type TLoginResponse = {
  access_token: string;
};

type TRegisterResponse = {
  data: Record<string, unknown>;
  status_code: number;
};

type TLogin = {
  email: string;
  password: string;
};

type TRegister = {
  username: string;
  email: string;
  password: string;
};

export default function Home() {
  const { isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();

  // Separate state for form toggle (true = register, false = login)
  const [showRegister, setShowRegister] = useState(false);

  const { execute: executeRegister, loading: registerLoading } =
    useApiRequest<TRegisterResponse>();

  const { execute: executeLogin, loading: loginLoading } =
    useApiRequest<TLoginResponse>();

  const [loginPayload, setLoginPayload] = useState<TLogin>({
    email: "",
    password: "",
  });

  const [registerPayload, setRegisterPayload] = useState<TRegister>({
    username: "",
    email: "",
    password: "",
  });

  // Redirect authenticated users
  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      router.push("/dashboard");
    }
  }, [isAuthenticated, authLoading, router]);

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Don't render auth forms if user is authenticated
  if (isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  const handleLoginChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setLoginPayload((prev) => ({
      ...prev,
      [name]: lodash.escape(value),
    }));
  };

  const handleRegistrationChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = event.target;
    setRegisterPayload((prev) => ({
      ...prev,
      [name]: lodash.escape(value),
    }));
  };

  const handleLoginSubmit = async () => {
    try {
      if (!API_URL) throw new Error("API URL is missing");

      const response = await executeLogin({
        url: `${API_URL}/users/login`,
        method: "POST",
        payload: loginPayload,
        requiresAuth: false,
      });

      if (response?.access_token) {
        setCookie("access-token", response.access_token);
        // Note: You might want to update auth context here too
        router.push("/dashboard");
      } else {
        alert("Login failed. Please try again.");
      }
    } catch (e) {
      console.error("Login error:", e);
      alert("Login failed. Please check your credentials.");
    }
  };

  const handleRegistrationSubmit = async () => {
    try {
      if (!API_URL) throw new Error("API URL is missing");

      const response = await executeRegister({
        url: `${API_URL}/users/register`,
        method: "POST",
        payload: registerPayload,
        requiresAuth: false,
      });

      if (response?.status_code === 201) {
        alert("Registration successful! Please login.");
        setShowRegister(false); // Switch to login form
      } else {
        alert("Registration failed. Please try again.");
      }
    } catch (e) {
      console.error("Registration error:", e);
      alert("Registration failed. Please try again.");
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 w-screen h-dvh overflow-hidden">
      {/* Desktop Image Section */}
      <div className="hidden lg:block">
        <ImageTransition />
      </div>

      {/* Main Content Section */}
      <div className="relative flex items-center justify-center lg:bg-gradient-to-br lg:from-slate-500 lg:to-slate-800">
        {/* Mobile Background Image */}
        <div className="absolute inset-0 lg:hidden">
          <ImageTransition />
        </div>

        {/* Mobile Overlay */}
        <div className="absolute inset-0 bg-black/60 lg:hidden" />

        {/* Form Container */}
        <div className="relative z-10 w-full max-w-md mx-auto p-6">
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-2xl p-8">
            {showRegister ? (
              // Registration Form
              <>
                <div className="text-center mb-8">
                  <h1 className="text-2xl font-bold text-gray-800 mb-2">
                    Welcome to my Blog
                  </h1>
                  <p className="text-gray-700">
                    Sign up now! to get the latest stories
                  </p>
                </div>

                <form
                  className="space-y-6"
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleRegistrationSubmit();
                  }}
                >
                  <div className="relative">
                    <div className="flex items-center border-2 border-gray-200 rounded-lg focus-within:border-blue-500 transition-colors bg-white/50">
                      <div className="px-3 py-3 border-r border-gray-200">
                        <span className="text-gray-600 text-lg">👤</span>
                      </div>
                      <input
                        id="username"
                        name="username"
                        onChange={handleRegistrationChange}
                        type="text"
                        placeholder="Username"
                        className="flex-1 px-4 py-3 text-gray-800 placeholder-gray-500 bg-transparent focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div className="relative">
                    <div className="flex items-center border-2 border-gray-200 rounded-lg focus-within:border-blue-500 transition-colors bg-white/50">
                      <div className="px-3 py-3 border-r border-gray-200">
                        <span className="text-gray-600 text-lg">📧</span>
                      </div>
                      <input
                        onChange={handleRegistrationChange}
                        id="email"
                        type="email"
                        name="email"
                        placeholder="Email address"
                        className="flex-1 px-4 py-3 text-gray-800 placeholder-gray-500 bg-transparent focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div className="relative">
                    <div className="flex items-center border-2 border-gray-200 rounded-lg focus-within:border-blue-500 transition-colors bg-white/50">
                      <div className="px-3 py-3 border-r border-gray-200">
                        <span className="text-gray-600 text-lg">🔒</span>
                      </div>
                      <input
                        onChange={handleRegistrationChange}
                        id="password"
                        type="password"
                        name="password"
                        placeholder="Password"
                        className="flex-1 px-4 py-3 text-gray-800 placeholder-gray-500 bg-transparent focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <button
                    disabled={registerLoading}
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg"
                  >
                    {registerLoading ? "Loading..." : "Sign up"}
                  </button>

                  <div className="text-center space-y-2">
                    <div className="text-sm text-gray-700">
                      Already have an account?{" "}
                      <button
                        disabled={registerLoading}
                        type="button"
                        onClick={() => setShowRegister(false)}
                        className="text-blue-600 hover:text-blue-700 font-medium transition-colors underline-offset-2 hover:underline"
                      >
                        Sign in
                      </button>
                    </div>
                  </div>
                </form>
              </>
            ) : (
              // Login Form
              <>
                <div className="text-center mb-8">
                  <h1 className="text-2xl font-bold text-gray-800 mb-2">
                    Welcome Back
                  </h1>
                  <p className="text-gray-700">Sign in to your account</p>
                </div>

                <form
                  className="space-y-6"
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleLoginSubmit();
                  }}
                >
                  <div className="relative">
                    <div className="flex items-center border-2 border-gray-200 rounded-lg focus-within:border-blue-500 transition-colors bg-white/50">
                      <div className="px-3 py-3 border-r border-gray-200">
                        <span className="text-gray-600 text-lg">📧</span>
                      </div>
                      <input
                        onChange={handleLoginChange}
                        id="email"
                        type="email"
                        name="email"
                        placeholder="Email address"
                        className="flex-1 px-4 py-3 text-gray-800 placeholder-gray-500 bg-transparent focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <div className="relative">
                    <div className="flex items-center border-2 border-gray-200 rounded-lg focus-within:border-blue-500 transition-colors bg-white/50">
                      <div className="px-3 py-3 border-r border-gray-200">
                        <span className="text-gray-600 text-lg">🔒</span>
                      </div>
                      <input
                        onChange={handleLoginChange}
                        id="password"
                        type="password"
                        name="password"
                        placeholder="Password"
                        className="flex-1 px-4 py-3 text-gray-800 placeholder-gray-500 bg-transparent focus:outline-none"
                        required
                      />
                    </div>
                  </div>

                  <button
                    disabled={loginLoading}
                    type="submit"
                    className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg"
                  >
                    {loginLoading ? "Loading..." : "Sign In"}
                  </button>

                  <div className="text-center space-y-2">
                    <div className="text-sm text-gray-700">
                      Do not have an account?{" "}
                      <button
                        disabled={loginLoading}
                        type="button"
                        onClick={() => setShowRegister(true)}
                        className="text-blue-600 hover:text-blue-700 font-medium transition-colors underline-offset-2 hover:underline"
                      >
                        Sign up
                      </button>
                    </div>
                  </div>
                </form>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
