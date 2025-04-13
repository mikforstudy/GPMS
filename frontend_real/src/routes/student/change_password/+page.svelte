<script>
    import { onMount } from "svelte";
    import axios from "axios";
    import { tick } from 'svelte';

    let username = "";
    let oldPassword = "";
    let newPassword = "";
    let confirmPassword = "";
    let loading = false;
    let errorMessage = "";
    let successMessage = "";
    let showOldPassword = false;
    let showNewPassword = false;
    let showConfirmPassword = false;

    // 表单验证状态
    let formValid = false;
    let passwordsMatch = true;
    let passwordError = "";

    onMount(() => {
        if (typeof window !== "undefined") {
            username = localStorage.getItem("username") || "";
        }
    });

    // 验证表单
    function validateForm() {
        passwordsMatch = newPassword === confirmPassword;
        passwordError = "";
        
        if (!oldPassword) {
            passwordError = "请输入当前密码";
            formValid = false;
            return;
        }
        
        if (!newPassword) {
            passwordError = "请输入新密码";
            formValid = false;
            return;
        }
        
        if (newPassword.length < 6) {
            passwordError = "新密码长度至少为6位";
            formValid = false;
            return;
        }
        
        if (!confirmPassword) {
            passwordError = "请确认新密码";
            formValid = false;
            return;
        }
        
        if (!passwordsMatch) {
            passwordError = "两次输入的密码不一致";
            formValid = false;
            return;
        }

        formValid = true;
    }

    // 提交表单
    async function handleSubmit() {
        validateForm();
        
        if (!formValid) {
            return;
        }
        
        loading = true;
        errorMessage = "";
        successMessage = "";
        
        try {
            const response = await axios.put(
                `http://127.0.0.1:8000/api/v1/users/change_password/${username}`,
                {
                    old_password: oldPassword,
                    new_password: newPassword
                }
            );
            
            successMessage = "密码修改成功！";
            oldPassword = "";
            newPassword = "";
            confirmPassword = "";
            
            // 3秒后清除成功消息
            setTimeout(() => {
                successMessage = "";
                tick();
            }, 3000);
            
        } catch (error) {
            console.error("Error changing password:", error);
            errorMessage = error.response?.data?.detail || "密码修改失败";
        } finally {
            loading = false;
        }
    }
</script>

<div class="flex justify-center items-center my-8">
    <div class="card w-full max-w-md bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title text-2xl font-bold">修改密码</h2>
            
            {#if errorMessage}
                <div class="alert alert-error shadow-lg">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>{errorMessage}</span>
                    </div>
                </div>
            {/if}
            
            {#if successMessage}
                <div class="alert alert-success shadow-lg">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        <span>{successMessage}</span>
                    </div>
                </div>
            {/if}
            
            {#if passwordError}
                <div class="alert alert-warning shadow-lg">
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                        <span>{passwordError}</span>
                    </div>
                </div>
            {/if}
            
            <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">用户名</span>
                    </label>
                    <input 
                        type="text" 
                        class="input input-bordered w-full" 
                        bind:value={username}
                        disabled
                    />
                </div>
                
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">当前密码</span>
                    </label>
                    <div class="input-group">
                        <input 
                            type={showOldPassword ? "text" : "password"} 
                            class="input input-bordered w-full" 
                            placeholder="请输入当前密码"
                            bind:value={oldPassword} 
                            on:input={validateForm}
                        />
                        <button 
                            type="button"
                            class="btn btn-square btn-outline"
                            on:click={() => showOldPassword = !showOldPassword}
                        >
                            {#if showOldPassword}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                            {/if}
                        </button>
                    </div>
                </div>
                
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">新密码</span>
                    </label>
                    <div class="input-group">
                        <input 
                            type={showNewPassword ? "text" : "password"} 
                            class="input input-bordered w-full" 
                            placeholder="请输入新密码（至少6位）"
                            bind:value={newPassword} 
                            on:input={validateForm}
                        />
                        <button 
                            type="button"
                            class="btn btn-square btn-outline"
                            on:click={() => showNewPassword = !showNewPassword}
                        >
                            {#if showNewPassword}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                            {/if}
                        </button>
                    </div>
                </div>
                
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">确认新密码</span>
                    </label>
                    <div class="input-group">
                        <input 
                            type={showConfirmPassword ? "text" : "password"} 
                            class="input input-bordered w-full" 
                            placeholder="请再次输入新密码"
                            bind:value={confirmPassword} 
                            on:input={validateForm}
                        />
                        <button 
                            type="button"
                            class="btn btn-square btn-outline"
                            on:click={() => showConfirmPassword = !showConfirmPassword}
                        >
                            {#if showConfirmPassword}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                            {:else}
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                            {/if}
                        </button>
                    </div>
                </div>
                
                <div class="form-control mt-6">
                    <button 
                        type="submit" 
                        class="btn btn-primary w-full"
                        disabled={loading}
                    >
                        {#if loading}
                            <span class="loading loading-spinner loading-md mr-2"></span>
                            正在处理...
                        {:else}
                            修改密码
                        {/if}
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>