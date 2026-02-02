// Simple auth API endpoint to match expected Better Auth pattern

export async function GET(request: Request) {
  // Handle different auth-related GET requests
  const url = new URL(request.url);
  const path = url.pathname;

  if (path.includes('/session')) {
    // Return mock session data
    const token = request.headers.get('authorization')?.replace('Bearer ', '');

    if (token) {
      return new Response(JSON.stringify({
        user: {
          id: 'mock-user-id',
          email: 'user@example.com',
          name: 'Mock User'
        },
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString() // 7 days
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    } else {
      return new Response(JSON.stringify({ user: null }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  }

  return new Response(JSON.stringify({ error: 'Invalid endpoint' }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' }
  });
}

export async function POST(request: Request) {
  // Handle different auth-related POST requests
  const url = new URL(request.url);
  const path = url.pathname;

  if (path.includes('/signup') || path.includes('/register')) {
    // Handle sign up
    try {
      const body = await request.json();
      // Mock sign up implementation
      if (body.email && body.password) {
        return new Response(JSON.stringify({
          user: {
            id: 'mock-user-id-' + Date.now(),
            email: body.email,
            name: body.email.split('@')[0]
          },
          token: 'mock-jwt-token-' + Date.now()
        }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      } else {
        return new Response(JSON.stringify({ error: 'Email and password required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    } catch (e) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } else if (path.includes('/signin') || path.includes('/login')) {
    // Handle sign in
    try {
      const body = await request.json();
      // Mock sign in implementation
      if (body.email && body.password) {
        return new Response(JSON.stringify({
          user: {
            id: 'mock-user-id',
            email: body.email,
            name: body.email.split('@')[0]
          },
          token: 'mock-jwt-token-' + Date.now()
        }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      } else {
        return new Response(JSON.stringify({ error: 'Email and password required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    } catch (e) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
  } else if (path.includes('/signout') || path.includes('/logout')) {
    // Handle sign out
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(JSON.stringify({ error: 'Invalid endpoint' }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' }
  });
}