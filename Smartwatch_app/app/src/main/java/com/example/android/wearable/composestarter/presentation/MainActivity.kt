@file:OptIn(ExperimentalHorologistApi::class, ExperimentalWearFoundationApi::class)

package com.example.android.wearable.composestarter.presentation

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Build
import androidx.compose.material.icons.filled.Send
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.wear.compose.foundation.ExperimentalWearFoundationApi
import androidx.wear.compose.foundation.rememberActiveFocusRequester
import androidx.wear.compose.foundation.rotary.RotaryScrollableDefaults.behavior
import androidx.wear.compose.foundation.rotary.rotaryScrollable
import androidx.wear.compose.material.MaterialTheme
import androidx.wear.compose.material.Text
import androidx.wear.compose.material.TitleCard
import androidx.wear.compose.material.dialog.Dialog
import androidx.wear.compose.navigation.SwipeDismissableNavHost
import androidx.wear.compose.navigation.composable
import androidx.wear.compose.navigation.rememberSwipeDismissableNavController
import androidx.wear.compose.ui.tooling.preview.WearPreviewDevices
import androidx.wear.compose.ui.tooling.preview.WearPreviewFontScales
import com.example.android.wearable.composestarter.R
import com.example.android.wearable.composestarter.presentation.theme.WearAppTheme
import com.google.android.horologist.annotations.ExperimentalHorologistApi
import com.google.android.horologist.compose.layout.AppScaffold
import com.google.android.horologist.compose.layout.ScalingLazyColumn
import com.google.android.horologist.compose.layout.ScalingLazyColumnDefaults
import com.google.android.horologist.compose.layout.ScalingLazyColumnDefaults.ItemType
import com.google.android.horologist.compose.layout.ScreenScaffold
import com.google.android.horologist.compose.layout.rememberResponsiveColumnState
import com.google.android.horologist.compose.material.AlertContent
import com.google.android.horologist.compose.material.Button
import com.google.android.horologist.compose.material.Chip
import com.google.android.horologist.compose.material.ListHeaderDefaults.firstItemPadding
import com.google.android.horologist.compose.material.ResponsiveListHeader
import org.eclipse.paho.client.mqttv3.*
import androidx.compose.runtime.rememberCoroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.coroutines.Dispatchers

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            WearApp()
        }
    }
}

@Composable
fun WearApp() {
    val navController = rememberSwipeDismissableNavController()

    WearAppTheme {
        AppScaffold {
            SwipeDismissableNavHost(navController = navController, startDestination = "menu") {
                composable("menu") {
                    GreetingScreen(
                        "Lucas",
                        onShowList = { navController.navigate("list") }
                    )
                }
                composable("list") {
                    ListScreen()
                }
            }
        }
    }
}

@Composable
fun GreetingScreen(greetingName: String, onShowList: () -> Unit) {
    val scrollState = rememberScrollState()

    /* If you have enough items in your list, use [ScalingLazyColumn] which is an optimized
     * version of LazyColumn for wear devices with some added features. For more information,
     * see d.android.com/wear/compose.
     */
    ScreenScaffold(scrollState = scrollState) {
        val padding = ScalingLazyColumnDefaults.padding(
            first = ItemType.Text,
            last = ItemType.Chip
        )()
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(scrollState)
                .rotaryScrollable(
                    behavior(scrollableState = scrollState),
                    focusRequester = rememberActiveFocusRequester()
                )
                .padding(padding),
            verticalArrangement = Arrangement.Center
        ) {
            Greeting(greetingName = greetingName)
            Chip(label = "Conectar a broker MQTT", onClick = onShowList)
        }
    }
}

@Composable
fun ListScreen() {
    var showDialog by remember { mutableStateOf(false) }
    var connectionStatus by remember { mutableStateOf("Desconectado") }
    var receivedMessage by remember { mutableStateOf("Nenhuma mensagem recebida") }
    val coroutineScope = rememberCoroutineScope()
    var mqttClient: MqttClient? = remember { null }

    val columnState = rememberResponsiveColumnState(
        contentPadding = ScalingLazyColumnDefaults.padding(
            first = ItemType.Text,
            last = ItemType.SingleButton
        )
    )

    ScreenScaffold(scrollState = columnState) {
        ScalingLazyColumn(
            columnState = columnState
        ) {
            item {
                ResponsiveListHeader(contentPadding = firstItemPadding()) {
                    Text(text = "Header")
                }
            }
            item {
                TitleCard(title = { Text("Título do card") }, onClick = { }) {
                    Text("Exemplo de conteúdo")
                }
            }
            item {
                Chip(label = "Exemplo de botão que faz nada", onClick = {
                    coroutineScope.launch {
                        val status = connectToMQTTBroker(
                            onMessageReceived = { message ->
                                coroutineScope.launch(Dispatchers.Main) {
                                    receivedMessage = message
                                }
                            },
                            onClientCreated = { client ->
                                mqttClient = client
                            }
                        )
                        connectionStatus = status
                    }
                })
            }
            item {
                Button(
                    imageVector = Icons.AutoMirrored.Filled.Send, // Ícone obrigatório para a API do Horologist
                    contentDescription = "Enviar Mensagem MQTT",
                    onClick = {
                        coroutineScope.launch(Dispatchers.IO) {
                            mqttClient?.let { client ->
                                publishMessage(client, "enviar", "Mensagem de teste MQTT")
                            }
                        }
                    }
                )
            }

            item {
                Text(text = "Status da conexão: $connectionStatus")
            }
            item {
                Text(text = receivedMessage)
            }
            item {
                Button(
                    imageVector = Icons.Default.Build,
                    contentDescription = "Exemplo de botão com ícone",
                    onClick = { showDialog = true }
                )
            }
        }
    }

    SampleDialog(
        showDialog = showDialog,
        onDismiss = { showDialog = false },
        onCancel = {},
        onOk = {}
    )
}

fun connectToMQTTBroker(onMessageReceived: (String) -> Unit, onClientCreated: (MqttClient) -> Unit): String {
    return try {
        val brokerUrl = "tcp://192.168.18.16:1883" // Substituir pelo broker desejado
        val clientId = MqttClient.generateClientId()
        val mqttClient = MqttClient(brokerUrl, clientId, null)
        val options = MqttConnectOptions()
        options.isAutomaticReconnect = true
        options.isCleanSession = true
        mqttClient.connect(options)

        mqttClient.subscribe("receber") { topic, message ->
            onMessageReceived(String(message.payload))
        }

        onClientCreated(mqttClient)
        "Conectado ao broker MQTT"
    } catch (e: MqttException) {
        "Falha na conexão: ${e.message}"
    }
}

fun publishMessage(mqttClient: MqttClient, topic: String, message: String) {
    try {
        val mqttMessage = MqttMessage()
        mqttMessage.payload = message.toByteArray()
        mqttClient.publish(topic, mqttMessage)
    } catch (e: MqttException) {
        e.printStackTrace()
    }
}


@Composable
fun Greeting(greetingName: String) {
    ResponsiveListHeader(contentPadding = firstItemPadding()) {
        Text(
            modifier = Modifier.fillMaxWidth(),
            textAlign = TextAlign.Center,
            color = MaterialTheme.colors.primary,
            text = stringResource(R.string.hello_world, greetingName)
        )
    }
}

@Composable
fun SampleDialog(
    showDialog: Boolean,
    onDismiss: () -> Unit,
    onCancel: () -> Unit,
    onOk: () -> Unit
) {
    val state = rememberResponsiveColumnState()

    Dialog(
        showDialog = showDialog,
        onDismissRequest = onDismiss,
        scrollState = state.state
    ) {
        SampleDialogContent(onCancel, onDismiss, onOk)
    }
}

@Composable
fun SampleDialogContent(
    onCancel: () -> Unit,
    onDismiss: () -> Unit,
    onOk: () -> Unit
) {
    AlertContent(
        icon = {},
        title = "Title",
        onCancel = {
            onCancel()
            onDismiss()
        },
        onOk = {
            onOk()
            onDismiss()
        }
    ) {
        item {
            Text(text = "Você clicou no botão de ferramenta.")
        }
    }
}

@WearPreviewDevices
@WearPreviewFontScales
@Composable
fun GreetingScreenPreview() {
    GreetingScreen("Preview Android", onShowList = {})
}

@WearPreviewDevices
@WearPreviewFontScales
@Composable
fun ListScreenPreview() {
    ListScreen()
}
