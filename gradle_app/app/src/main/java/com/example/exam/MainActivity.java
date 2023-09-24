package com.example.exam;

import android.os.Bundle;

import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.firebase.database.ChildEventListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;


public class MainActivity extends AppCompatActivity {
    boolean live = true;
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("message");
    DatabaseReference myRefNick = database.getReference("nickname");

    private static final short MAX_MESSAGE_LENGTH = 255;
    private static final short MAX_NICKNAME_LENGTH = 255;
    EditText mEditTextMessage, mEditNickname;
    TextView mTimeTextView;
    Button mSendButton;
    RecyclerView mMessageRecycler;
    ArrayList<String> messages = new ArrayList<>();
    ArrayList<String> nicknames = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        // Найти элементы пользовательского интерфейса по их идентификаторам
        mSendButton = findViewById(R.id.send_message_b);
        mEditTextMessage = findViewById(R.id.message_input);
        mEditNickname = findViewById(R.id.nickname_input);

        mTimeTextView = (TextView) findViewById(R.id.time);

        // Установить таймер для обновления времени
        new Timer().scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        fetchTime();
                    }
                });
            }
        }, 0, 1000);

        mMessageRecycler = findViewById(R.id.message_recycler);
        mMessageRecycler.setLayoutManager(new LinearLayoutManager(this));

        // Создать адаптер для списка сообщений и имен пользователей
        DataAdapter dataAdapter = new DataAdapter(this, messages, nicknames);
        mMessageRecycler.setAdapter(dataAdapter);

        // Установить слушатель нажатия на кнопку "Отправить"
        mSendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String msg = mEditTextMessage.getText().toString();
                String nick = mEditNickname.getText().toString();
                String time = mTimeTextView.getText().toString();
                nick = nick + " " + time; // Решил, что будет проще просто соединить никнейм и время
                                          // вместо хранения дополнительного массива под время

                // Проверяем, что сообщение и никнейм не пустые
                if (msg.equals("") || nick.equals("")) {
                    Toast.makeText(MainActivity.this,R.string.empty_message_error, Toast.LENGTH_SHORT).show();
                    return;
                }

                // Проверяем, что длина сообщения и никнейма не превышает максимально допустимую
                if (msg.length() > MAX_MESSAGE_LENGTH || nick.length() > MAX_NICKNAME_LENGTH) {
                    Toast.makeText(MainActivity.this, R.string.length_message_error, Toast.LENGTH_SHORT).show();
                    return;
                }

                // Отправляем сообщение и никнейм в базу данных
                myRef.push().setValue(msg);
                myRefNick.push().setValue(nick);
                mEditTextMessage.setText("");
            }
        });

        // Добавляем слушатель событий для базы данных Firebase Realtime Database для получения новых сообщений
        myRef.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {
                // Получаем новое сообщение и добавляем его в список сообщений
                String msg = snapshot.getValue(String.class);
                messages.add(msg);
                dataAdapter.notifyDataSetChanged();
            }

            @Override
            public void onChildChanged(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {

            }

            @Override
            public void onChildRemoved(@NonNull DataSnapshot snapshot) {

            }

            @Override
            public void onChildMoved(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {

            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
        myRefNick.addChildEventListener(new ChildEventListener() {
            @Override
            public void onChildAdded(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {
                String nick = snapshot.getValue(String.class);
                nicknames.add(nick);
                // Уведомляем адаптер о том, что данные изменились и прокручиваем список к последнему сообщению
                dataAdapter.notifyDataSetChanged();
                mMessageRecycler.smoothScrollToPosition(nicknames.size());
            }

            @Override
            public void onChildChanged(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {

            }

            @Override
            public void onChildRemoved(@NonNull DataSnapshot snapshot) {

            }

            @Override
            public void onChildMoved(@NonNull DataSnapshot snapshot, @Nullable String previousChildName) {

            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

    }

    // Метод для получения текущего времени с сервера
    // используя Retrofit для выполнения HTTP-запроса и получения JSON-ответа
    void fetchTime() {
        // Создание объекта Retrofit и настройка базового URL-адреса для API
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("http://date.jsontest.com/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        // Создание объекта для вызова метода API
        JsontestAPI api = retrofit.create(JsontestAPI.class);
        Call<ServerTime> serverTimeCall = api.getServerDateTime();

        // Выполнение запроса асинхронно и обработка ответа или ошибки через колбэки
        serverTimeCall.enqueue(new Callback<ServerTime>() {
            @Override
            public void onResponse(Call<ServerTime> call, Response<ServerTime> response) {
                // Получение объекта ServerTime из тела ответа
                ServerTime serverTime = response.body();
                // Установка полученного времени в TextView
                mTimeTextView.setText(serverTime.getTime());
            }

            @Override
            public void onFailure(Call<ServerTime> call, Throwable t) {
                // Обработка ошибки при выполнении запроса
                Toast.makeText(getApplicationContext(),
                        "Error" + t.toString(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}