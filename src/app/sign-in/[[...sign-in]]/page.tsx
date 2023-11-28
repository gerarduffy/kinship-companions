import { SignIn, useUser } from "@clerk/nextjs";
import { useEffect } from "react";
import { useRouter } from "next/router";

export default function Page() {
  const { user } = useUser();
  const router = useRouter();

  // Redirect the user to the main application when they sign in
  useEffect(() => {
    if (user) {
      router.push("/");
    }
  }, [user, router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <SignIn />
    </div>
  );
}