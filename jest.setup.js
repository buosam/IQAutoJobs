
import '@testing-library/jest-dom'
import { TextEncoder, TextDecoder } from 'util';

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Polyfill for the Response object
if (!global.Response) {
  global.Response = class Response {
    constructor(body, init) {
      this.body = body;
      this.status = init?.status || 200;
      this.headers = new Headers(init?.headers);
      this.ok = this.status >= 200 && this.status < 300;
    }

    async text() {
      return Promise.resolve(this.body || '');
    }

    async json() {
      return Promise.resolve(JSON.parse(this.body || '{}'));
    }
  };
}

if (!global.Headers) {
  global.Headers = class Headers {
    constructor(init) {
      this._headers = {};
      if (init) {
        for (const [key, value] of Object.entries(init)) {
          this._headers[key.toLowerCase()] = value;
        }
      }
    }

    get(name) {
      return this._headers[name.toLowerCase()];
    }
  };
}
