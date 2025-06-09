import { useAuth } from "@/context/authContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Dashboard() {
  const { isAuthenticated, loading, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Redirect unauthenticated users to login
    if (!loading && !isAuthenticated) {
      router.push("/");
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Don't render anything while redirecting
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h2 className="text-lg font-semibold text-blue-800 mb-2">
                Authentication Status
              </h2>
              <p className="text-blue-700">
                Status:{" "}
                {isAuthenticated ? "Authenticated" : "Not Authenticated"}
              </p>
            </div>

            {user && (
              <div className="bg-green-50 p-4 rounded-lg">
                <h2 className="text-lg font-semibold text-green-800 mb-2">
                  User Information
                </h2>
                <div className="space-y-2 text-green-700">
                  <p>
                    <strong>Role:</strong> {user.role}
                  </p>
                  <p>
                    <strong>User ID:</strong> {user.user_id}
                  </p>
                </div>
              </div>
            )}

            <div className="bg-gray-50 p-4 rounded-lg">
              <h2 className="text-lg font-semibold text-gray-800 mb-2">
                Quick Actions
              </h2>
              <div className="space-x-4">
                <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                  View Profile
                </button>
                <button className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                  Settings
                </button>
                <button
                  onClick={() => {
                    // Add logout functionality here
                    console.log("Logout clicked");
                  }}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
