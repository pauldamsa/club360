<template>
    <div class="p-6 max-w-4xl mx-auto">
        <!-- Add success messages at the top -->
        <div v-if="successMessage" class="mb-4 p-4 bg-green-100 text-green-700 rounded-lg">
            {{ successMessage }}
        </div>
        <Card class="bg-white shadow-lg">
            <div class="p-6 space-y-8">
                <!-- Club Info Section -->
                <div>
                    <h2 class="text-xl font-semibold mb-4">Club Information</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <FormControl
                            label="Club Email"
                            type="email"
                            v-model="profileData.email"
                            :disabled="true"
                        />
                        <FormControl
                            label="First Name"
                            type="text"
                            v-model="profileData.first_name"
                            :disabled="true"
                        />
                        <FormControl
                            label="Last Name"
                            type="text"
                            v-model="profileData.last_name"
                            :disabled="true"
                        />
                    </div>
                </div>

                <!-- Password Change Section -->
                <div>
                    <h2 class="text-xl font-semibold mb-4">Change Password</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="relative">
                            <FormControl
                                :type="showNewPassword ? 'text' : 'password'"
                                label="New Password"
                                v-model="passwordData.new"
                                :error="passwordErrors.new"
                            />
                            <button 
                                type="button"
                                class="absolute right-3 top-1/2 transform translate-y-1 text-gray-500"
                                @click="showNewPassword = !showNewPassword"
                            >
                                <FeatherIcon :name="showNewPassword ? 'eye-off' : 'eye'" class="w-4 h-4" />
                            </button>
                        </div>
                        <div class="relative">
                            <FormControl
                                :type="showConfirmPassword ? 'text' : 'password'"
                                label="Confirm New Password"
                                v-model="passwordData.confirm"
                                :error="passwordErrors.confirm"
                            />
                            <button 
                                type="button"
                                class="absolute right-3 top-1/2 transform translate-y-1 text-gray-500"
                                @click="showConfirmPassword = !showConfirmPassword"
                            >
                                <FeatherIcon :name="showConfirmPassword ? 'eye-off' : 'eye'" class="w-4 h-4" />
                            </button>
                        </div>
                        <div class="flex items-end">
                            <Button
                                label="Change Password"
                                variant="solid"
                                :loading="changePasswordResource.loading"
                                @click="handlePasswordChange"
                            />
                        </div>
                    </div>
                </div>

                <!-- Default Stock Values Section -->
                <div>
                    <h2 class="text-xl font-semibold mb-4">Default Stock Products Servings</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <FormControl
                            label="Formula 1 (Shake)"
                            type="number"
                            v-model="settingsData.shake"
                            min="0"
                        />
                        <FormControl
                            label="Herbal Tea"
                            type="number"
                            v-model="settingsData.tea"
                            min="0"
                        />
                        <FormControl
                            label="Aloe"
                            type="number"
                            v-model="settingsData.aloe"
                            min="0"
                        />
                        <FormControl
                            label="PDM"
                            type="number"
                            v-model="settingsData.pdm"
                            min="0"
                        />
                    </div>
                </div>

                <!-- Save Button -->
                <div class="flex justify-end pt-4 border-t">
                    <Button
                        label="Save Changes"
                        variant="solid"
                        :loading="saveChangesResource.loading"
                        @click="handleSaveChanges"
                    />
                </div>
            </div>
        </Card>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { Card, FormControl, Button, createResource, FeatherIcon } from 'frappe-ui';
import { useRoute } from 'vue-router';
const route = useRoute();

const profileData = ref({
    email: '',
    first_name: '',
    last_name: ''
});

const passwordData = ref({
    new: '',
    confirm: ''
});

const passwordErrors = ref({
    new: '',
    confirm: ''
});

const settingsData = ref({
    shake: 0,
    tea: 0,
    aloe: 0,
    pdm: 0
});

const successMessage = ref('');

const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

// Resource to load settings
const settingsResource = createResource({
    url: 'club360.api.get_club_settings',
    auto: true,
    onSuccess: (data) => {
        settingsData.value = data;
        // profileData.value.email = data.email;
    }
});

const userResource = createResource({
    url: 'club360.api.get_club_user',
    auto: true,
    onSuccess: (data) => {
        profileData.value.email = data.email;
        profileData.value.first_name = data.first_name;
        profileData.value.last_name = data.last_name;
    }
});

// Resource to change password
const changePasswordResource = createResource({
    url: 'club360.api.change_club_password',
    makeParams() {
        return {
            new_password: passwordData.value.new
        }
    },
    onSuccess: () => {
        passwordData.value = { new: '', confirm: '' };
        successMessage.value = 'Password changed successfully';
        // Clear message after 3 seconds
        setTimeout(() => {
            successMessage.value = '';
        }, 3000);
    },
    onError: (error) => {
        passwordErrors.value.new = error.message;
    }
});

// Resource to save changes
const saveChangesResource = createResource({
    url: 'club360.api.update_club_settings',
    makeParams() {
        return {
            new_settings: settingsData.value
        };
    },
    onSuccess: () => {
        successMessage.value = 'Settings saved successfully';
        // Clear message after 3 seconds
        setTimeout(() => {
            successMessage.value = '';
        }, 3000);
    }
});

function handlePasswordChange() {
    // Reset errors
    passwordErrors.value = { new: '', confirm: '' };

    // Validate
    if (!passwordData.value.new) {
        passwordErrors.value.new = 'New password is required';
        return;
    }
    if (passwordData.value.new !== passwordData.value.confirm) {
        passwordErrors.value.confirm = 'Passwords do not match';
        return;
    }

    changePasswordResource.submit();
}

function handleSaveChanges() {
    saveChangesResource.submit();
}
</script>