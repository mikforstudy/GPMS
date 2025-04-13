import { json } from '@sveltejs/kit';

import { redirect } from '@sveltejs/kit';

export function load() {
    throw redirect(302, '/login');
}
