import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, RouterProvider } from 'react-router-dom';

// Perfect Scrollbar
import 'react-perfect-scrollbar/dist/css/styles.css';

// Tailwind css
import './tailwind.css';

// i18n (needs to be bundled)
import './i18n';

// Router
import router from './router/index';

// Redux
import { Provider } from 'react-redux';
import store from './store/index';
import { QueryClient, QueryClientProvider } from 'react-query';
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <QueryClientProvider client={queryClient}>
        <Provider store={store}>
            <RouterProvider router={router} />
        </Provider>
    </QueryClientProvider>

);
