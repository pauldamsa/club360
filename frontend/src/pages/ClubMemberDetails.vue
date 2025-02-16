<template>
    <div class="p-6">
        <!-- Header section -->
        <div class="mb-8 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <Avatar :label="clubMemberDoc.full_name" size="xl" />
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">{{ clubMemberDoc.full_name }}</h1>
                </div>
            </div>
            <div class = "flex items-center space-x-4">
                <Button variant="solid" label="Edit Member" />
                <Button variant="solid" label="Add Membership" />
            </div>
        </div>

        <!-- Main content -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Member Details Card -->
            <Card class="lg:col-span-1">
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div class="text-gray-500">First Name</div>
                        <div>{{ clubMemberDoc.first_name }}</div>
                        
                        <div class="text-gray-500">Last Name</div>
                        <div>{{ clubMemberDoc.last_name }}</div>
                        
                        <div class="text-gray-500">Coach</div>
                        <div>
                            <Badge :label="clubMemberDoc.coach" />
                        </div>
                        
                        <div class="text-gray-500">Source</div>
                        <div>{{ clubMemberDoc.source }}</div>
                        
                        <div class="text-gray-500">Referrals</div>
                        <div>{{ clubMemberDoc.referrals }}</div>
                    </div>
                </div>
            </Card>

            <!-- Memberships Card -->
            <Card class="lg:col-span-2">
                <template #header>
                    <div class="flex justify-between items-center">
                        <h2 class="text-lg font-medium">Memberships</h2>
                        <Button variant="outline" label="Add Membership" />
                    </div>
                </template>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Start Date</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">End Date</th>
                                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Remaining Visits</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="membership in membershipsList" :key="membership.name" class="hover:bg-gray-50">
                                <td class="px-4 py-3">
                                    {{ membership.type }}
                                </td>
                                <td class="px-4 py-3">{{ formatDate(membership.start_date) }}</td>
                                <td class="px-4 py-3">{{ formatDate(membership.end_date) }}</td>
                                <td class="px-4 py-3">
                                    <Badge :label="membership.remaining_visits" variant="solid" 
                                        :class="{
                                            'bg-green-100 text-green-800': membership.remaining_visits > 5,
                                            'bg-yellow-100 text-yellow-800': membership.remaining_visits <= 5 && membership.remaining_visits > 0,
                                            'bg-red-100 text-red-800': membership.remaining_visits === 0
                                        }"
                                    />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    </div>
</template>

<script setup>
import { createDocumentResource, Card, Badge, Avatar, Button } from 'frappe-ui';
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();

const clubMemberResource = createDocumentResource({
    doctype: 'Club Member',
    name: route.params.full_name,
    fields: ['*'],
    auto: true,
})

const membershipsList = computed(() => {
    if (clubMemberResource.doc?.memberships) {
        return clubMemberResource.doc.memberships;
    }
    return [];
});

const clubMemberDoc = computed(() => {
    if (clubMemberResource.doc) {
        return clubMemberResource.doc;
    }
    return {};
});

function formatDate(date) {
    return new Date(date).toLocaleDateString();
}
</script>