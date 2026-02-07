import { NextRequest, NextResponse } from 'next/server';

// Define protected routes
const protectedRoutes = ['/tasks', '/chat'];

export function proxy(request: NextRequest) {
  // For now, we'll implement a basic check
  // In a real implementation, this would check for auth tokens

  // Check if the requested path is a protected route
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // If it's a protected route, check for session
  if (isProtectedRoute) {
    // In a real implementation, we would check for auth token here
    // For now, we'll allow everything through for development
    // This will be enhanced when we integrate with Better Auth

    // If no session found, redirect to sign-in
    // const token = request.cookies.get('better-auth-session-token');
    // if (!token) {
    //   return NextResponse.redirect(new URL('/signin', request.url));
    // }
  }

  return NextResponse.next();
}

// Specify which routes the proxy should run on
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};