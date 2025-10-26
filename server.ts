// server.ts - Next.js Standalone + Socket.IO
import { setupSocket } from '@/lib/socket';
import { createServer } from 'http';
import { Server } from 'socket.io';
import next from 'next';
import { createProxyMiddleware } from 'http-proxy-middleware';

const dev = process.env.NODE_ENV !== 'production';
const currentPort = parseInt(process.env.PORT || '5000', 10);
const hostname = '0.0.0.0';
const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';

// Custom server with Socket.IO integration
async function createCustomServer() {
  try {
    // Create Next.js app
    const nextApp = next({ 
      dev,
      dir: process.cwd(),
      // In production, use the current directory where .next is located
      conf: dev ? undefined : { distDir: './.next' }
    });

    await nextApp.prepare();
    const handle = nextApp.getRequestHandler();

    // Create a proxy middleware
    const apiProxy = createProxyMiddleware({
      target: backendUrl,
      changeOrigin: true,
      pathRewrite: { '^/api': '/api' },
      ws: true, // proxy websockets
      logLevel: 'debug',
    });

    // Create HTTP server that will handle both Next.js and Socket.IO
    const server = createServer((req, res) => {
      if (req.url?.startsWith('/api') || req.url?.startsWith('/healthz') || req.url?.startsWith('/readiness') || req.url?.startsWith('/metrics')) {
        // Let the proxy handle API requests
        return apiProxy(req, res, () => {});
      }
      // Skip socket.io requests from Next.js handler
      if (req.url?.startsWith('/api/socketio')) {
        return;
      }
      handle(req, res);
    });

    // Setup Socket.IO
    const io = new Server(server, {
      path: '/api/socketio',
      cors: {
        origin: "*",
        methods: ["GET", "POST"]
      }
    });

    setupSocket(io);

    // Start the server
    server.listen(currentPort, hostname, () => {
      console.log(`> Ready on http://${hostname}:${currentPort}`);
      console.log(`> Socket.IO server running at ws://${hostname}:${currentPort}/api/socketio`);
    });

  } catch (err) {
    console.error('Server startup error:', err);
    process.exit(1);
  }
}

// Start the server
createCustomServer();
