<template>
    <div class="p-6">
        <!-- Coach Details Header -->
        <Card class="mb-8">
            <div class="p-6 flex items-center justify-between">
                <div class="flex items-center space-x-6">
                    <Avatar :label="coachDoc.full_name" size="2xl" class="ring-4 ring-white shadow-lg" />
                    <div class="space-y-3">
                        <div>
                            <h1 class="text-2xl font-bold text-gray-900">{{ coachDoc.full_name }}</h1>
                            <div class="flex items-center space-x-3 mt-2">
                                <Badge :label="coachDoc.role" variant="outline" theme="red"/>
                                <Badge :label="coachDoc.level" variant="solid"/>
                            </div>
                        </div>
                        <div class="flex items-center space-x-4 text-gray-600">
                            <div class="flex items-center space-x-2">
                                <FeatherIcon name="hash" class="w-4 h-4"/>
                                <span>{{ coachDoc.id_herbalife || 'No ID' }}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <FeatherIcon name="phone" class="w-4 h-4"/>
                                <span>{{ coachDoc.phone_number || 'No phone' }}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <FeatherIcon name="mail" class="w-4 h-4"/>
                                <span>{{ coachDoc.email || 'No email' }}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <Button variant="solid" label="Edit Coach" icon="edit-2" @click="handleEditCoach" />
            </div>
        </Card>
        <!-- Lists Section -->
        <div class="space-y-6">
            <!-- Club Members -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Club Members</h2>
                        <Badge :label="clubMembers.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <table class="min-w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="member in clubMembers" :key="member.name" class="hover:bg-gray-50">
                                <td class="py-2">
                                    <div class="flex items-center">
                                        <Avatar :label="member.full_name" size="sm" class="mr-2" />
                                        <span>{{ member.full_name }}</span>
                                    </div>
                                </td>
                                <td class="py-2 text-right">{{ member.source }}</td>
                                <td class="py-2 text-right"><Badge :label="member.status" /></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>

            <!-- Trainees -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Trainees</h2>
                        <Badge :label="trainees.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <table class="min-w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="trainee in trainees" :key="trainee.name" class="hover:bg-gray-50">
                                <td class="py-2">
                                    <div class="flex items-center">
                                        <Avatar :label="trainee.full_name" size="sm" class="mr-2" />
                                        <span>{{ trainee.full_name }}</span>
                                    </div>
                                </td>
                                <td class="py-2 text-right">{{ trainee.role }}</td>
                                <td class="py-2 text-right"><Badge :label="trainee.level" /></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>

            <!-- Junior Partners -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Junior Partners</h2>
                        <Badge :label="juniorPartners.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <table class="min-w-full">
                        <tbody class="divide-y divide-gray-200">
                            <tr v-for="partner in juniorPartners" :key="partner.name" class="hover:bg-gray-50">
                                <td class="py-2">
                                    <div class="flex items-center">
                                        <Avatar :label="partner.full_name" size="sm" class="mr-2" />
                                        <span>{{ partner.full_name }}</span>
                                    </div>
                                </td>
                                <td class="py-2 text-right">{{ partner.role }}</td>
                                <td class="py-2 text-right"><Badge :label="partner.level" /></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    </div>
    <EditCoachDialog ref="editCoachDialog" />
</template>

<script setup>
import { createDocumentResource, createListResource, Card, Badge, Avatar, Button, FeatherIcon } from 'frappe-ui';
import { useRoute } from 'vue-router';
import { computed, ref } from 'vue';
import EditCoachDialog from '@/components/EditCoachDialog.vue';

const route = useRoute();

const coachResource = createDocumentResource({
    doctype: 'Coach',
    name: route.params.full_name,
    fields: ['*'],
    auto: true,
});

const coachDoc = computed(() => coachResource.doc || {});

const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name', 'status', 'source'],
    filters: { coach: route.params.full_name },
    auto: true
});

const traineesResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'level', 'role'],
    filters: { role: 'Trainee', sponsor: route.params.full_name },
    auto: true
});

const juniorPartnersResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'level', 'role'],
    filters: { role: 'Junior Partner', sponsor: route.params.full_name },
    auto: true
});

const clubMembers = computed(() => clubMembersResource.list.data || []);
const trainees = computed(() => traineesResource.list.data || []);
const juniorPartners = computed(() => juniorPartnersResource.list.data || []);

const editCoachDialog = ref(null);

function handleEditCoach() {
    editCoachDialog.value?.openDialog(coachDoc.value);
}
</script>