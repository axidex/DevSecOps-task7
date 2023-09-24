package com.example.exam;

import android.view.View;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import org.w3c.dom.Text;

public class ViewHolder extends RecyclerView.ViewHolder {
    TextView message;
    TextView nickname;

    public ViewHolder(@NonNull View itemView) {
        super(itemView);
        message = itemView.findViewById(R.id.message_item);
        nickname = itemView.findViewById(R.id.nickname);
    }
}
