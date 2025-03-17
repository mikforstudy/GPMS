import { items } from './data.js'

export function load() {
    return {
        summaires: items.map((item) => ({
            slug: item.slug,
            title: item.title
        }))
    };
}