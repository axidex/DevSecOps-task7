package com.example.exam;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;


public class DataAdapter extends RecyclerView.Adapter<ViewHolder> {

    ArrayList<String> messages;
    ArrayList<String> nicknames;
    LayoutInflater inflater;
    public DataAdapter(Context context, ArrayList<String> messages, ArrayList<String> nicknames) {
        this.nicknames = nicknames;
        this.messages = messages;
        this.inflater = LayoutInflater.from(context);
    }

    // метод создания нового ViewHolder
    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        // загружаем макет элемента списка и передаем его в конструктор ViewHolder
        View view = inflater.inflate(R.layout.item_message, parent, false);

        return new ViewHolder(view);
    }

    // метод для привязки данных к элементам списка
    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        // если список сообщений или никнеймов пустой, то просто выходим из метода
        if(messages.size()*nicknames.size() == 0)
            return;
        String msg = messages.get(position);
        String nick = nicknames.get(position);

        holder.message.setText(msg);
        holder.nickname.setText(nick);
    }

    // метод для получения количества элементов списка
    @Override
    public int getItemCount() {
        return nicknames.size();
    }
}
