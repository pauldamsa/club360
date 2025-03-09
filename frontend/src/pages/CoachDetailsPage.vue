<template>
    <div class="p-4 md:p-6">
        <!-- Coach Details Header -->
        <Card class="mb-4 md:mb-8">
            <div class="p-4 flex flex-col sm:flex-row sm:items-center justify-between space-y-4 sm:space-y-0">
                <div class="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-6">
                    <Avatar :label="coachDoc.full_name" size="xl" class="self-center sm:self-auto ring-4 ring-white shadow-lg" />
                    <div class="space-y-3 text-center sm:text-left">
                        <div>
                            <h1 class="text-xl md:text-2xl font-bold text-gray-900">{{ coachDoc.full_name }}</h1>
                            <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2 mt-2">
                                <Badge :label="coachDoc.role" variant="outline" theme="red"/>
                                <Badge :label="coachDoc.level" variant="solid"/>
                            </div>
                        </div>
                        <div class="flex flex-col sm:flex-row items-center gap-3 text-gray-600 text-sm">
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
                <Button 
                    variant="solid" 
                    label="Edit Coach" 
                    icon="edit-2" 
                    @click="handleEditCoach"
                    class="w-full sm:w-auto"
                />
            </div>
        </Card>

        <!-- Lists Section -->
        <div class="space-y-4 md:space-y-6">
            <!-- Club Members -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Club Members</h2>
                        <Badge :label="clubMembers.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <!-- Mobile View - with scrolling -->
                    <div class="block sm:hidden">
                        <div class="overflow-y-auto max-h-80 pr-2 space-y-3">
                            <div v-for="member in clubMembers" 
                                :key="member.name" 
                                class="border rounded-lg p-3"
                            >
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <Avatar :label="member.full_name" size="sm" />
                                        <div>
                                            <div class="font-medium">{{ member.full_name }}</div>
                                            <div class="text-sm text-gray-500">{{ member.source }}</div>
                                        </div>
                                    </div>
                                    <Badge :label="member.status" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Desktop View - with scrolling -->
                    <div class="hidden sm:block overflow-y-auto max-h-96">
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
                </div>
            </Card>

            <!-- Trainees -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Trainees</h2>
                        <Badge :label="trainees.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <!-- Mobile View -->
                    <div class="block sm:hidden space-y-3">
                        <div v-for="trainee in trainees" 
                             :key="trainee.name" 
                             class="border rounded-lg p-3"
                        >
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <Avatar :label="trainee.full_name" size="sm" />
                                    <div>
                                        <div class="font-medium">{{ trainee.full_name }}</div>
                                        <div class="text-sm text-gray-500">{{ trainee.role }}</div>
                                    </div>
                                </div>
                                <Badge :label="trainee.level" />
                            </div>
                        </div>
                    </div>
                    <!-- Desktop View -->
                    <div class="hidden sm:block">
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
                </div>
            </Card>

            <!-- Junior Partners -->
            <Card>
                <div class="p-4">
                    <div class="flex items-center space-x-3 mb-4">
                        <h2 class="text-lg font-medium">Junior Partners</h2>
                        <Badge :label="juniorPartners.length" variant="outline" class="bg-red-100 text-red-800" size="lg" />
                    </div>
                    <!-- Mobile View -->
                    <div class="block sm:hidden space-y-3">
                        <div v-for="partner in juniorPartners" 
                             :key="partner.name" 
                             class="border rounded-lg p-3"
                        >
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <Avatar :label="partner.full_name" size="sm" />
                                    <div>
                                        <div class="font-medium">{{ partner.full_name }}</div>
                                        <div class="text-sm text-gray-500">{{ partner.role }}</div>
                                    </div>
                                </div>
                                <Badge :label="partner.level" />
                            </div>
                        </div>
                    </div>
                    <!-- Desktop View -->
                    <div class="hidden sm:block">
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
                </div>
            </Card>

            <!-- Stock Management Section -->
            <Card v-if="showStockSection">
                <div class="p-4">
                    <h2 class="text-lg font-medium mb-4">Stock Management</h2>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
                        <!-- Shake -->
                        <div class="flex flex-col items-center space-y-2">
                            <CupSoda class="w-20 h-20 text-gray-600" />
                            <span class="font-medium text-gray-700">Formula 1</span>
                            <div class="flex items-center space-x-2">
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.shake = Math.max(0, stockData.shake - 1)"
                                >
                                    <MinusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                                <Input
                                    type="number"
                                    v-model="stockData.shake"
                                    class="w-16 text-center"
                                    min="0"
                                    placeholder="0"
                                />
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.shake++"
                                >
                                    <PlusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                            </div>
                            <span class="text-sm text-gray-500">Pieces</span>
                        </div>

                        <!-- Tea -->
                        <div class="flex flex-col items-center space-y-2">
                            <Coffee class="w-20 h-20 text-gray-600" />
                            <span class="font-medium text-gray-700">Herbal Tea</span>
                            <div class="flex items-center space-x-2">
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.tea = Math.max(0, stockData.tea - 1)"
                                >
                                    <MinusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                                <Input
                                    type="number"
                                    v-model="stockData.tea"
                                    class="w-16 text-center"
                                    min="0"
                                    placeholder="0"
                                />
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.tea++"
                                >
                                    <PlusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                            </div>
                            <span class="text-sm text-gray-500">Pieces</span>
                        </div>

                        <!-- Aloe -->
                        <div class="flex flex-col items-center space-y-2">
                            <Milk class="w-20 h-20 text-gray-600" />
                            <span class="font-medium text-gray-700">Aloe Concentrate</span>
                            <div class="flex items-center space-x-2">
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.aloe = Math.max(0, stockData.aloe - 1)"
                                >
                                    <MinusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                                <Input
                                    type="number"
                                    v-model="stockData.aloe"
                                    class="w-16 text-center"
                                    min="0"
                                    placeholder="0"
                                />
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.aloe++"
                                >
                                    <PlusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                            </div>
                            <span class="text-sm text-gray-500">Pieces</span>
                        </div>

                        <!-- PDM -->
                        <div class="flex flex-col items-center space-y-2">
                            <GlassWater class="w-20 h-20 text-gray-600" />
                            <span class="font-medium text-gray-700">PDM</span>
                            <div class="flex items-center space-x-2">
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.pdm = Math.max(0, stockData.pdm - 1)"
                                >
                                    <MinusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                                <Input
                                    type="number"
                                    v-model="stockData.pdm"
                                    class="w-16 text-center"
                                    min="0"
                                    placeholder="0"
                                />
                                <button
                                    class="p-1 rounded hover:bg-gray-100 border"
                                    @click="stockData.pdm++"
                                >
                                    <PlusIcon class="w-4 h-4 text-gray-600" />
                                </button>
                            </div>
                            <span class="text-sm text-gray-500">Pieces</span>
                        </div>
                    </div>
                    <div class="flex justify-end mt-4">
                        <Button
                            variant="solid"
                            label="Add Stock"
                            @click="addStock"
                            class="w-full sm:w-auto"
                        />
                    </div>
                </div>
            </Card>
        </div>
    </div>
    <EditCoachDialog ref="editCoachDialog" />

    <!-- Stock Confirmation Dialog -->
    <Dialog
        :options="{
            title: 'Confirm Stock Addition',
            actions: [
                {
                    label: 'Cancel',
                    variant: 'outline',
                    onClick: () => showStockConfirmationDialog = false
                },
                {
                    label: 'Confirm',
                    variant: 'solid',
                    onClick: confirmAddStock
                }
            ]
        }"
        v-model="showStockConfirmationDialog"
    >
        <template #body-content>
            <div class="space-y-4">
                <h3 class="font-medium">Please confirm the following stock quantities:</h3>
                <div class="grid grid-cols-2 gap-4">
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <div class="text-sm text-gray-600">Formula 1</div>
                        <div class="text-lg font-medium">{{ stockData.shake }}</div>
                    </div>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <div class="text-sm text-gray-600">Herbal Tea</div>
                        <div class="text-lg font-medium">{{ stockData.tea }}</div>
                    </div>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <div class="text-sm text-gray-600">Aloe</div>
                        <div class="text-lg font-medium">{{ stockData.aloe }}</div>
                    </div>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <div class="text-sm text-gray-600">PDM</div>
                        <div class="text-lg font-medium">{{ stockData.pdm }}</div>
                    </div>
                </div>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { createDocumentResource, createListResource, Card, Badge, Avatar, Button, FeatherIcon, Dialog, Input, createResource } from 'frappe-ui';
import { useRoute } from 'vue-router';
import { computed, ref } from 'vue';
import EditCoachDialog from '@/components/EditCoachDialog.vue';
import { PlusIcon, MinusIcon, Coffee, Milk, GlassWater, CupSoda } from 'lucide-vue-next';

const route = useRoute();

const coachResource = createDocumentResource({
    doctype: 'Coach',
    name: route.params.id_herbalife,
    fields: [
        'full_name',
        'role',
        'level',
        'id_herbalife',
        'phone_number',  
        'email',         
        'sponsor',
        'stock'
    ],
    auto: true,
});
const coachDoc = computed(() => coachResource.doc || {});

const clubMembersResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name', 'status', 'source'],
    filters: { 
        coach: route.params.id_herbalife,
        type: 'Club Member' 
    },
    auto: true
});

const traineesResource = createListResource({
    doctype: 'Club Member',
    fields: ['full_name', 'status', 'source'],
    filters: { 
        coach: route.params.id_herbalife,
        type: 'Trainee' 
    },
    auto: true
});

const juniorPartnersResource = createListResource({
    doctype: 'Coach',
    fields: ['full_name', 'level', 'role'],
    filters: { role: 'Junior Partner', sponsor: route.params.id_herbalife },
    auto: true
});

const clubMembers = computed(() => clubMembersResource.list.data || []);
const trainees = computed(() => traineesResource.list.data || []);
const juniorPartners = computed(() => juniorPartnersResource.list.data || []);

const editCoachDialog = ref(null);

function handleEditCoach() {
    editCoachDialog.value?.openDialog(coachDoc.value);
}

const stockData = ref({
    shake: 0,
    tea: 0,
    aloe: 0,
    pdm: 0
});

// Add dialog state
const showStockConfirmationDialog = ref(false);

function addStock() {
    showStockConfirmationDialog.value = true;
}

const addStockResource = createResource({
    url: 'club360.api.add_stock',
    makeParams: () => ({
        stock_data: {
            coach: route.params.id_herbalife,
            ...stockData.value
        }
    }),
    onSuccess: () => {
        showStockConfirmationDialog.value = false;
        stockData.value = { shake: 0, tea: 0, aloe: 0, pdm: 0 };
        // Reload coach data to show updated stock
        coachResource.reload();
    },
    onError: (error) => {
        console.error('Error adding stock:', error);
    }
});

function confirmAddStock() {
    addStockResource.submit();
}

// Add computed property to check if stock section should be shown
const showStockSection = computed(() => {
    const role = coachDoc.value?.role;
    return role === 'Junior Partner' || role === 'Club Owner';
});
</script>