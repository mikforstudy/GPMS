import { writable } from 'svelte/store';
import { goto } from '$app/navigation';

// 创建用户状态存储
export const user = writable(typeof localStorage !== 'undefined' ? JSON.parse(localStorage.getItem('user')) : null);

// 订阅状态变化，同步到localStorage
user.subscribe((value) => {
    if (typeof localStorage !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(value));
    }
});

// 登出函数
export const logout = () => {
    user.set(null);
    if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('user');
    }
    goto('/login');
}; 