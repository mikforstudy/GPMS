import { error } from '@sveltejs/kit';
import {items} from '../data.js';

export function load({params}) {
    const item = items.find((item)=>item.slug === params.slug);

    if(!item) error(404)

    return {
        item
    };
}